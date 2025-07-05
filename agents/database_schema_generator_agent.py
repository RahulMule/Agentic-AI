from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq
from tools.rag import get_parsed_requirements,generate_schema_from_parsed_requirements, query_rag
from llama_index.llms.ollama import Ollama
from config.settings import settings
class schemageneratoragent:
    systmPrompt  = """
        You are the SchemaDesignerAgent.

        Your job begins by calling the tool: `get_parsed_requirements_from_context_store` to fetch parsed requirements.

        Once you retrieve the data, analyze the software requirements and generate a clean, structured database schema in JSON format by tool call generate_schema_from_parsed_requirements()

        🧠 You are NOT generating Python or SQL code — your job is to create a language-agnostic schema blueprint, which will later be used to generate SQLAlchemy or Pydantic models.

        ---

        Your output must be a JSON object with the following structure:

        {
        "entities": [
            {
            "name": "EntityName",
            "description": "A short description of the entity",
            "fields": [
                {
                "name": "field_name",
                "type": "string | integer | float | boolean | datetime | enum | foreign_key",
                "nullable": true | false,
                "primary_key": true | false,
                "unique": true | false,
                "description": "Short explanation of the field"
                }
            ],
            "relationships": [
                {
                "type": "one-to-many | many-to-one | many-to-many",
                "target": "OtherEntityName",
                "field": "foreign_key_field_name"
                }
            ]
            }
        ]
        }

        ---

        💡 Rules:
        - Assume types will later be mapped to SQLAlchemy types (e.g., `string` → `String`, `datetime` → `DateTime`)
        - Only include fields and relationships directly inferred from the requirements
        - If a relationship is implied (e.g., an Order belongs to a User), include it
        - Think step by step — validate each field type and relationship for realism

        ✅ Once the schema is ready, hand off control to the `APISpecGeneratorAgent`.
        """

    #llm = Ollama(model="codellama:7b-python",request_timeout=120.0)
    llm = Groq(model=settings.grok_model_name,api_key=settings.groq_api_key,parallel_tool_calls=True)
    database_schema_generator_agent = FunctionAgent(
        name="database_schema_generator_agent",
        description="This agent is useful to generate database schema and entity relationships from function requirements",
        system_prompt=systmPrompt,
        tools=[
            FunctionTool.from_defaults(fn=get_parsed_requirements),
            FunctionTool.from_defaults(fn=generate_schema_from_parsed_requirements),
            FunctionTool.from_defaults(fn=query_rag)      
        ],
        function_call_mode="sequential",
        llm = llm,

    )