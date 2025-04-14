from profsandman_agents.embedders import SentenceTransformerEmbedder
from profsandman_agents.llms import OpenAILLM
from profsandman_agents.vector_databases import ChromaDBVectorDB
from profsandman_agents.agents import MultiAgent, ChromaAgent, SQLiteAgent, ExcelAgent

# Load API key
with open("data/API_KEY.txt", "r") as f:
    api_key = f.read()

llm = OpenAILLM(api_key=api_key)

embedder = SentenceTransformerEmbedder()
vdb = ChromaDBVectorDB(
    dbpath="data/monza_2024_corpus",
    embedder=embedder,
    distance_measure="cosine"
)
vdb.initialize_db()
vdb.initialize_collection("semanticchunker_db")

# Optional: Print document count
try:
    collection = vdb.collection_
    if collection:
        print(f"🔍 ChromaDB contains {collection.count()} documents.")
    else:
        print("⚠️ No collection initialized.")
except Exception as e:
    print(f"⚠️ Error checking ChromaDB documents: {e}")

rag_agent = ChromaAgent(llm, vdb)
rag_kwargs = {"k": 5, "max_distance": 0.75, "show_citations": True}

sql_agent = SQLiteAgent(
    llm,
    database_url="data/Structured_Data.db",
    db_desc="""The database contains structured data from the 2024 Italian Grand Prix at Monza.
- Team: contains team names and IDs.
- Driver: contains driver names, IDs, and associated teams.
- RaceResults: final positions, laps, time gaps, and points for each driver.
- QualifyingResults: qualifying session data per driver.
- TimingData: lap-by-lap performance with timestamps, speed, and sector times.
Most tables can be joined using a common driver_id or team_id field.""",
    include_detail=True
)
sql_kwargs = {"view_sql": True}

xl_agent = ExcelAgent(
    llm,
    database_url="data/monza_data.xlsx",
    xl_desc="This file contains Monza race data from 2024.",
    include_detail=True
)
xl_kwargs = {"view_sql": True}

multi_agent = MultiAgent(
    llm,
    agent_names=["Rag Agent", "SQL Agent", "Excel Agent"],
    agents=[rag_agent, sql_agent, xl_agent],
    agent_descriptions=[
        "Answer questions using documents and interviews",
        "Answer questions using SQL race data",
        "Answer questions using structured Excel data"
    ],
    agent_query_kwargs=[rag_kwargs, sql_kwargs, xl_kwargs]
)

def query_race_agent(user_input):
    try:
        response = multi_agent.query(user_input)

        agent_used = getattr(multi_agent, "last_agent_name_", "Unknown")
        agent_type = type(getattr(multi_agent, "last_agent_", None)).__name__

        trace = "Trace not available."

        if agent_type in ["SQLiteAgent", "ExcelAgent"]:
            trace = getattr(multi_agent.last_agent_, "response_", None)
            trace = getattr(trace, "sql_query", "SQL trace not found.") if trace else "No SQL trace available."
        elif agent_type == "ChromaAgent":
            trace = "\n\n".join(getattr(multi_agent.last_agent_, "docs_", []))

        formatted_trace = f"🔎 **Agent Used:** {agent_used}\n\n{trace}"
        return response, formatted_trace

    except Exception as e:
        return "An error occurred while querying the chatbot.", f"❌ Error: {str(e)}"
