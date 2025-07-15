from llama_index.core.agent.workflow import AgentWorkflow, AgentInput, AgentOutput, ToolCall, ToolCallResult, AgentStream
from agents.requirements_parser import Requirement_parser
from agents.database_schema_generator_agent import schemageneratoragent
from agents.api_spec_generator import APISpecGeneratorAgent
from agents.code_generation_agent import CodeGenerationAgent


async def main():
    openapi_spec_agent = APISpecGeneratorAgent().get_agent()
    code_generation_agent = CodeGenerationAgent().get_agent()
    agent_workflow = AgentWorkflow(
        agents=[Requirement_parser.requirementParse_agent, schemageneratoragent.database_schema_generator_agent,openapi_spec_agent,code_generation_agent],
        root_agent= "requirementParse_agent",
        initial_state={
            "requirementParse_agent":"requirementParse_agent is not completed yet",
            "database_schema_generator_agent":"database_schema_generator_agent is not completed yet",
            "APISpecGeneratorAgent":"APISpecGeneratorAgent is not completed yet"
        }
    )

    handler =  agent_workflow.run(
 """Please index the legacy code, parse all functional requirements, generate a database schema, OpenAPI specifications,rest api(FastAPI code) for the backend."""
    )


    current_agent = None
    current_tool_calls = ""
    async for event in handler.stream_events():
        if (
            hasattr(event, "current_agent_name")
            and event.current_agent_name != current_agent
        ):
            current_agent = event.current_agent_name
            print(f"\n{'='*50}")
            print(f"🤖 Agent: {current_agent}")
            print(f"{'='*50}\n")

        if isinstance(event, AgentStream):
            if event.delta:
                print(event.delta, end="", flush=True)
        elif isinstance(event, AgentInput):
             print("📥 Input:", event.input)
        elif isinstance(event, AgentOutput):
            if event.response.content:
                print("📤 Output:", event.response.content)
            if event.tool_calls:
                print(
                    "🛠️  Planning to use tools:",
                    [call.tool_name for call in event.tool_calls],
                )
        elif isinstance(event, ToolCallResult):
            print(f"🔧 Tool Result ({event.tool_name}):")
            print(f"  Arguments: {event.tool_kwargs}")
            print(f"  Output: {event.tool_output}")
        elif isinstance(event, ToolCall):
            print(f"🔨 Calling Tool: {event.tool_name}")
            print(f"  With arguments: {event.tool_kwargs}")



            
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())