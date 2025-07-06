from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from tools.rag import query_rag,get_query_index,write_requirements_to_context_store, write_to_txt_file
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq
from agents.database_schema_generator_agent import schemageneratoragent
from config.settings import settings

from pathlib import Path
class Requirement_parser:


    llm = Ollama(model="mistral", request_timeout=120,)
    def load_prompt(file_name: str) -> str:
        return Path(f"./prompts/{file_name}").read_text(encoding="utf-8")
    
    system_prompt = load_prompt("requirement_parser_prompt.txt")

    #llm = Groq(model= settings.grok_model_name,api_key= settings.groq_api_key)

    requirementParse_agent = FunctionAgent(
        name="requirementParse_agent",
        description="This agent will be starter point of whole project. The agent will be useful to parse functional requirement document and perform indexing to query later",\
        system_prompt=system_prompt,
        llm=llm,
        tools=[
            FunctionTool.from_defaults(fn=get_query_index,return_direct=True),
            FunctionTool.from_defaults(fn=query_rag,return_direct=True),
            FunctionTool.from_defaults(fn=write_to_txt_file,return_direct=True),
            FunctionTool.from_defaults(name="write_requirements_to_context_store",
                                        description="Save the compiled requirement sections for further use",
                                        fn=write_requirements_to_context_store,),
        ],
        function_call_mode="sequential",
        max_function_calls_per_step=1,
        can_handoff_to=["database_schema_generator_agent"]
    )

