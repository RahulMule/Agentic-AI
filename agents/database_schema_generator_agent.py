from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq
from tools.rag import get_parsed_requirements,generate_schema_from_parsed_requirements, query_rag
from llama_index.llms.ollama import Ollama
from pathlib import Path
from config.settings import settings
class schemageneratoragent:

    def load_prompt(file_name: str) -> str:
        return Path(f"./prompts/{file_name}").read_text(encoding="utf-8")
    
    system_prompt = load_prompt("database_schema_generator.txt")

    #llm = Ollama(model="mistral",request_timeout=120.0)
    #llm = Groq(model=settings.grok_model_name,api_key=settings.groq_api_key,parallel_tool_calls=True)
    llm = Groq(model= "mistral-saba-24b",api_key= settings.groq_api_key)
    database_schema_generator_agent = FunctionAgent(
        name="database_schema_generator_agent",
        description="This agent is useful to generate database schema and entity relationships from function requirements",
        system_prompt= system_prompt,
        tools=[
            FunctionTool.from_defaults(fn=get_parsed_requirements),
            FunctionTool.from_defaults(fn=generate_schema_from_parsed_requirements),
            FunctionTool.from_defaults(fn=query_rag)   
        ],
        function_call_mode="sequential",
        llm = llm,
        can_handoff_to=["APISpecGeneratorAgent"]

    )