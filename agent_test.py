import sys
sys.path.append(r"C:\Users\sophi\OneDrive\Documents\GitHub\LLM-Agent-4420\profsandman_agents")

from profsandman_agents.embedders import SentenceTransformerEmbedder
from profsandman_agents.llms import OpenAILLM
from profsandman_agents.agents import SQLiteAgent, ExcelAgent

# Load your API key
with open("data/API_KEY.txt", "r") as f:
    api_key = f.read()

llm = OpenAILLM(api_key=api_key)

sql_agent = SQLiteAgent(
    llm,
    database_url="data/Structured_Data.db",
    db_desc="F1 race results and drivers from Monza 2024",
    include_detail=True
)

xl_agent = ExcelAgent(
    llm,
    database_url="data/monza_data.xlsx",
    db_desc="F1 Monza 2024 Excel race data",
    include_detail=True
)

# 🔍 TEST SQL agent
print("\n--- SQL Agent Test ---")
try:
    response = sql_agent.query("Which team scored the most points?", view_sql=True)
    print("Response:\n", response)
except Exception as e:
    print("SQL Agent Error:", e)

# 🔍 TEST Excel agent
print("\n--- Excel Agent Test ---")
try:
    response = xl_agent.query("List all drivers from the Excel file", view_sql=True)
    print("Response:\n", response)
except Exception as e:
    print("Excel Agent Error:", e)
