from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from tools.rag import get_parsed_requirements,get_schema,write_apispec_to_txt_file
from config.settings import settings
class APISpecGeneratorAgent:
    def __init__(self):
        self.llm =  Groq(model = settings.grok_model_name,api_key=settings.groq_api_key)
    
    def get_agent(self):
        return FunctionAgent(
            name="APISpecGeneratorAgent",
            description="The agent is useful to build openapi specification for all the rest endpoints",
            llm=self.llm,
            system_prompt="""
            Get requirements context memory store using get_parsed_requirements function call, 
            database schema from local path using get_schema function call and 
            pass this to agent/llm to generate openapi specification document in yaml format. 
            once openapi specifications are generated, 
            store them in local path using write_openapi_to_txt_file at path './data/apisepc.yaml'
            handoff control to CodeGenerationAgent""",
            tools= [
                    FunctionTool.from_defaults(fn=get_parsed_requirements,return_direct=True),
                    FunctionTool.from_defaults(fn=get_schema,return_direct=True),
                    FunctionTool.from_defaults(fn=write_apispec_to_txt_file,return_direct=True),
                    ],
            function_call_mode="sequential",
            can_handoff_to=["CodeGenerationAgent"]
        )