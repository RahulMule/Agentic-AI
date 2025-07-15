from config.settings import settings
from llama_index.llms.groq import Groq
from tools.rag import write_code
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent
class CodeGenerationAgent:
    def __init__(self):
        #self.llm = Groq(model= settings.grok_model_name, api_key= settings.groq_api_key)
        self.llm  = Groq(model= "mistral-saba-24b",api_key= settings.groq_api_key)
    def get_agent(self):
        return FunctionAgent(
            name="CodeGenerationAgent",
            description="This agent is useful in generating fastapi code for the rest api based on provided fsd, parsed requirements, schema and openapi specifications",
            llm=self.llm,
            system_prompt="""
                         Write code to output directory using function write_code at path './data/output/'
                        """,
            tools=[
                   FunctionTool.from_defaults(fn=write_code,return_direct=True)
                   ],
            function_call_mode="sequential",
            can_handoff_to=[]
        )