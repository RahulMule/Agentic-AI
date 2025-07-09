from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from tools.rag import query_rag,index_legacy_code,write_requirements_to_context_store, write_to_txt_file
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq
from agents.database_schema_generator_agent import schemageneratoragent
from config.settings import settings

from pathlib import Path
class Requirement_parser:


    #llm = Ollama(model="mistral",  temperature=0.2, top_p=0.9,  request_timeout=120,)
    def load_prompt(file_name: str) -> str:
        return Path(f"./prompts/{file_name}").read_text(encoding="utf-8")
    
    system_prompt = load_prompt("requirement_parser_prompt.txt")

    #llm = Groq(model= settings.grok_model_name,api_key= settings.groq_api_key)
    llm = Groq(model= "mistral-saba-24b",api_key= settings.groq_api_key)

    requirementParse_agent = FunctionAgent(
        name="requirementParse_agent",
        description="The agent is helpful in indexing the legacy code, generate parsed functional requirements by quering the rag",\
        system_prompt=system_prompt,
        llm=llm,
        verbose=True,
        tools=[
            FunctionTool.from_defaults(fn=index_legacy_code),
            FunctionTool.from_defaults(fn=query_rag),
            FunctionTool.from_defaults(fn=write_to_txt_file),
        ],
        function_call_mode="sequential",
        can_handoff_to=["database_schema_generator_agent"]
    )

