from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings,StorageContext,load_index_from_storage
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from functools import lru_cache
from llama_index.core.query_engine import BaseQueryEngine
import os

PERSIST_DIR = "./index/"
DATA_DIR = "./data/fsd/"
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(
    model="mistral",
    request_timeout=120.0
)
def _get_query_engine() -> BaseQueryEngine:
    """Internal method to return query engine object (not exposed to agent)."""
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print("✅ Loading index from disk...")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    else:
        print("⚠️ Index not found — building and persisting...")
        documents = SimpleDirectoryReader(input_dir=DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        print("✅ Index built and saved.")

    return index.as_query_engine()

def get_query_index() -> str:
    """Agent tool: Index the data and return confirmation (does NOT return engine)."""
    _ = _get_query_engine()
    return "Indexing complete ✅"

def query_rag(query:str) -> str:
    """This function can be used to query the rag for any function requirement related questions by any agents. The rag will have fsd or functional requirement data indexed"""
    query_engine = _get_query_engine()
    response = query_engine.query(query)
    return str(response)

async def write_requirements_to_context_store(ctx: Context, fsd : str) -> str :
    """This function is useful when all the functional requirements are gathered and needs to be written in cotext store"""
    await ctx.store.set("requirements",fsd)
    #print(fsd)
    return "Parsed requirements stored in context memory store"

