from profsandman_agents.text_extractors import BaseTextExtractor
from profsandman_agents.chunkers import SemanticChunker
from profsandman_agents.embedders import SentenceTransformerEmbedder
from profsandman_agents.vector_databases import ChromaDBVectorDB
from profsandman_agents.llms import OpenAILLM
import os

# Create our own simple extractor with filenames for traceability
class SimpleTextExtractor(BaseTextExtractor):
    def extract(self, file_paths):
        docs = []
        for path in file_paths:
            with open(path, "r", encoding="utf-8") as f:
                docs.append({
                    "text": f.read(),
                    "metadata": {"source": os.path.basename(path)}  # ✅ Step 1: Add filename as metadata
                })
        return docs

# Setup
api_key = open(r"C:\Users\sophi\OneDrive - Marquette University\Desktop - Copy\Spring 2025\AIM 4420\API KEY.txt").read()
llm = OpenAILLM(api_key=api_key)

# Setup components
embedder = SentenceTransformerEmbedder()
text_extractor = SimpleTextExtractor()
chunker = SemanticChunker(llm)

vdb = ChromaDBVectorDB(
    dbpath="data/monza_2024_corpus",  # ✅ Use forward slashes or raw strings
    embedder=embedder,
    distance_measure="cosine",
    text_extractor=text_extractor,
    chunker=chunker
)

vdb.initialize_db()
vdb.initialize_collection("semanticchunker_db")

# Load all .txt files
folder_path = "data/monza_2024_corpus"
file_paths = [
    os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".txt")
]

# Add documents
vdb.add_to_collection(file_paths)
print("✅ Documents loaded successfully with traceability!")
