from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from tools.rag import query_rag,get_query_index,write_requirements_to_context_store, write_to_txt_file
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq
from agents.database_schema_generator_agent import schemageneratoragent
from config.settings import settings
class Requirement_parser:
    system_prompt = """
You are an agent named 'RequirementsParser'. Your only role is to extract requirement-related information from a Functional Specification Document (FSD) by calling the provided tools — one at a time.

⚠️ Do NOT write answers, summaries, or code. Only use the tools.

Follow this exact sequence:

1. Call the tool: get_query_index — to initialize the document index.
2. Then, for each of these questions, call query_rag with the question as input:
   - What are the system-level requirements?
   - What are the functional requirements?
   - What entities are described in the system?
   - What are the data models?
   - What are the roles and permissions?
   - What REST endpoints are proposed?
   - What validations and constraints exist?
   - What non-functional requirements are specified?

3. After collecting all answers, combine them into one formatted string with clear section headers.

4. Finally, call the tool: write_to_txt_file pass file path as './data/req.txt' and content as  the the output of step 3 and check the response. 
5. based on write_to_txt_file response handoff to next agent - database_schema_generator_agent
🚫 Do not output anything except tool calls.
🛠️ Only one tool call at a time. No skipping, no batching.
"""


    #llm = Ollama(model="codellama:7b-python", request_timeout=120,)
    llm = Groq(model= settings.grok_model_name,api_key= settings.groq_api_key)
    requirementParse_agent = FunctionAgent(
        name="requirementParse_agent",
        description="This agent will be starter point of whole project. The agent will be useful to parse functional requirement document and perform indexing to query later",\
        system_prompt=system_prompt,
        llm=llm,
        tools=[
            FunctionTool.from_defaults(fn=get_query_index),
            FunctionTool.from_defaults(fn=query_rag),
            FunctionTool.from_defaults(fn=write_to_txt_file),
            FunctionTool.from_defaults(name="write_requirements_to_context_store",
                                        description="Save the compiled requirement sections for further use",
                                        fn=write_requirements_to_context_store,),
        ],
        function_call_mode="sequential",
        can_handoff_to=["database_schema_generator_agent"]
        
    )

