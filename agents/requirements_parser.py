from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from tools.rag import query_rag,get_query_index,write_requirements_to_context_store
from llama_index.core.tools import FunctionTool
class Requirement_parser:
    system_prompt = """
You are the RequirementsParser agent.

Your ONLY responsibility is to call tools to extract requirement information from the FSD (Functional Specification Document).

⚠️ You are NOT allowed to write code or produce answers yourself.
✅ You MUST only call the tools provided to you.

Use this step-by-step process:

1. First, call `get_query_index` to initialize indexing.
2. Then for **each** of the following queries, call `query_rag` **with that query string as input** (do not call `query_rag` without a query):
   - "What are the system-level requirements?"
   - "What are the functional requirements?"
   - "What entities are described in the system?"
   - "What are the data models?"
   - "What are the roles and permissions?"
   - "What REST endpoints are proposed?"
   - "What validations and constraints exist?"
   - "What non-functional requirements are specified?"

3. After collecting results, concatenate them with clear section headers.

4. Call `write_requirements_to_context_store` with the full compiled string.

Your output must be in the form of tool calls only.

🔁 Call one tool at a time. Do not skip steps.
"""


    llm = Ollama(model="mistral",request_timeout=120.0)
    requirementParse_agent = FunctionAgent(
        name="requirementParse_agent",
        description="This agent will be starter point of whole project. The agent will be useful to parse functional requirement document and perform indexing to query later",\
        system_prompt=system_prompt,
        llm=llm,
        tools=[
            FunctionTool.from_defaults(fn=get_query_index),
            FunctionTool.from_defaults(fn=query_rag),
            FunctionTool.from_defaults(fn=write_requirements_to_context_store),
        ],
        function_call_mode="sequential"
    )

