from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from tools.rag import generate_openapi_specification
from config.settings import settings
class APISpecGeneratorAgent:
    def __init__(self):
        self.llm =  Groq(model = settings.grok_model_name,api_key=settings.groq_api_key)
        #self.llm  = Groq(model= "mistral-saba-24b",api_key= settings.groq_api_key)
    def get_agent(self):
        return FunctionAgent(
            name="APISpecGeneratorAgent",
            description="The agent is useful to build openapi specification for all the rest endpoints",
            llm=self.llm,
            system_prompt="""Generate OpenAPI Specifications in yaml format by calling generate_openapi_specification pass file_path as './data/output/OpenAPI/apisepc.yaml'""",
            tools= [
                    FunctionTool.from_defaults(fn=generate_openapi_specification)
                    ],
            function_call_mode="sequential",
            can_handoff_to=["CodeGenerationAgent"]
        )