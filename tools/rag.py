from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings,StorageContext,load_index_from_storage
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from functools import lru_cache
from llama_index.core.query_engine import BaseQueryEngine
import json, time, os
from llama_index.llms.groq import Groq
from config.settings import settings
from pathlib import Path

PERSIST_DIR = "./index/"
DATA_DIR = "./data/fsd/"
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(
    model="mistral",
    request_timeout=120.0
)
#Settings.llm = Groq(model=settings.grok_model_name,api_key=settings.groq_api_key,parallel_tool_calls=True)
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

def index_legacy_code() -> str:
    """Agent tool: Index the data and return confirmation (does NOT return engine)."""
    _ = _get_query_engine()
    return "Indexing complete ✅, continue with generating parsed functional specification document"

def query_rag(query:str) -> str:
    """This function can be used to query the rag for any function requirement related questions by any agents. The rag will have fsd or functional requirement data indexed"""
    query_engine = _get_query_engine()
    response = query_engine.query(query)
    write_to_txt_file("./data/req.txt",str(query))
    write_to_txt_file("./data/req.txt",str(response))
    return str(response)

async def write_requirements_to_context_store(ctx: Context, fsd : str) -> str :
    """This function is useful when all the functional requirements are gathered and need to be written in cotext store"""
    await ctx.store.set("requirements",fsd)
    print(fsd)
    return json.dumps({"status": "done", "next_agent": "database_schema_generator_agent"})

async def get_parsed_requirements() -> str:
    """This function is helpul in getting parsed requirements from local path"""
    #parsed_requirements = await ctx.store.get("requirements")
    return Path(f"./data/req.txt").read_text(encoding="utf-8")
async def generate_schema_from_parsed_requirements(parasedRequirements: str, ctx: Context) -> str:
    """This function is useful in generating database schema, entity relationships from parased requirements and storing it in memory context"""
    response = await Settings.llm.acomplete(f"generate database schema, entity relationships from functional requirements. This schema will be used in generating fastapi application later :" + parasedRequirements)
    await ctx.store.set("schema",str(response))
    return str(response)

def write_to_txt_file(file_path: str, content: str) -> str:
    """this method is useful in writing the agent output into local path

    Args:
        file_path (str): _description_
        content (str): _description_

    Returns:
        str: _description_
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)
        return  json.dumps({"status": "done", "next_agent": "database_schema_generator_agent"})
    except Exception as e:
        return f"Failed: {str(e)}"
    
def write_apispec_to_txt_file(file_path: str, content: str) -> str:
    """this method is useful in writing the api spec generator agent output into local path

    Args:
        file_path (str): _description_
        content (str): _description_

    Returns:
        str: _description_
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return str( json.dumps({"status": "done", "next_agent": "code_generation_agent"}))
    except Exception as e:
        return f"Failed: {str(e)}"

def get_schema(file_name: str) -> str:
        return Path(f"./data/{file_name}").read_text(encoding="utf-8")

def write_code(filename: str, code_content: str) -> str:
    """
    Writes the generated code to a file in the ./data/output/ directory.

    Args:
        filename (str): The name of the file to write (e.g., 'main.py').
        code_content (str): The code to write to the file.

    Returns:
        str: Success message or error message.
    """
    try:
        output_dir = './data/output'
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(code_content)

        return f"✅ Code successfully written to: {file_path}"
    except Exception as e:
        return f"❌ Failed to write code: {str(e)}"



