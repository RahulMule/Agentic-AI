from config.settings import settings
from llama_index.llms.groq import Groq
from tools.rag import write_code, get_schema, get_parsed_requirements
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent
class CodeGenerationAgent:
    def __init__(self):
        self.llm = Groq(model= settings.grok_model_name, api_key= settings.groq_api_key)
    def get_agent(self):
        return FunctionAgent(
            name="CodeGenerationAgent",
            description="This agent is useful in generating fastapi code for the rest api based on provided fsd, parsed requirements, schema and openapi specifications",
            llm=self.llm,
            system_prompt="""
                         Follow below steps
                         1. Get schema from local path using get_schema function call
                         2. Get requirements from './data/req.txt' with get_schema function call
                         3. Get openapi specification from path './data/apisepc.yaml' get_schema function call
                         4. Generate fastapi based code by passing all these files to llm to help generating code
                         5. Write code to output directory using function write_code at path './data/output/'
                        """,
            tools=[FunctionTool.from_defaults(fn=get_schema,return_direct=True),
                   FunctionTool.from_defaults(fn=get_parsed_requirements,return_direct=True),
                   FunctionTool.from_defaults(fn=write_code,return_direct=True)
                   ],
            function_call_mode="sequential",
            can_handoff_to=[]
        )