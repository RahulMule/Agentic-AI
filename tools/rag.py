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
    return "Indexing complete ✅"

async def query_rag(query:str,ctx: Context) -> str:
    """This function can be used to query the rag for any function requirement related questions by any agents. The rag will have fsd or functional requirement data indexed"""
    query_engine = _get_query_engine()
    response = query_engine.query(query)
    write_to_txt_file("./data/output/ParsedRequirements/req.txt",str(query))
    write_to_txt_file("./data/output/ParsedRequirements/req.txt",str(response))
    if(str(query)=="What non-functional requirements are specified?"):
        #ctx.store.set("requirementParse_agent","requirementParse_agent completed, call next agent")
        await ctx.store.set("requirementParse_agent","requirementParse_agent completed, call next agent")
    return str(response)

async def Update_workflow_context(ctx: Context, status_dict: dict) -> str :
    """
    Update the agent state in the context with the given status dictionary.

    Args:
        context: The agent workflow context object with `update_state` method.
        status_dict (dict): A dictionary where keys are agent names and values are status strings.

    Returns:
        str: A JSON-formatted string confirming the updated statuses.
    """
    try:
        if not isinstance(status_dict, dict):
            raise ValueError("status_dict must be a dictionary.")

        if ctx is None:
            raise ValueError("Context (ctx) was not provided.")

        for agent_name, status in status_dict.items():
            await ctx.store.set(agent_name, status)

        return json.dumps({
            "status": "success",
            "updated": status_dict
        })

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

def _get_parsed_requirements() -> str:
    """This function is helpul in getting parsed requirements from local path"""
    #parsed_requirements = await ctx.store.get("requirements")
    return Path(f"./data/output/ParsedRequirements/req.txt").read_text(encoding="utf-8")
async def generate_schema_from_parsed_requirements(ctx: Context) -> str:
    """This function is useful in generating database schema, entity relationships from parased requirements"""
    parsed_schema = _get_parsed_requirements()
    response = Settings.llm.complete(f"generate database schema, entity relationships from functional requirements. This schema will be used in generating fastapi application later :" + parsed_schema)
    print(str(response))
    write_to_txt_file("./data/output/schema/schema.txt",str(response))
    await ctx.store.set("database_schema_generator_agent","database_schema_generator_agent completed,call APISpecGeneratorAgent agent")
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
        print("inside write_to_txt_file0--")
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)
        return  json.dumps({"status": "done"})
    except Exception as e:
        return f"Failed: {str(e)}"
    
async def generate_openapi_specification(file_path: str, ctx: Context) -> str:
    """this method is useful in generating the api spec generator agent output into local path

    Args:
        file_path (str): _description_
        content (str): _description_

    Returns:
        str: _description_
    """
    try:
        database_schema = get_schema("schema.txt")
        parsed_requirements = _get_parsed_requirements()
        response = Settings.llm.complete(f"generate openapi specification document from parsed specification document:" + parsed_requirements + "and from database schema:" + database_schema + "return response in yaml format")
        ("Received response from llm to generate openapi spec")
        print(str(response))
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(response))
        await ctx.store.set("APISpecGeneratorAgent","APISpecGeneratorAgent completed,call next agent")
        return str(response)
    except Exception as e:
        return f"Failed: {str(e)}"

def get_schema(file_name: str) -> str:
        return Path(f"./data/output/schema/{file_name}").read_text(encoding="utf-8")

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



