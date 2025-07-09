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
        root_agent= "database_schema_generator_agent",
        initial_state={
            "requirements":[],
            "schema":[]
        }
    )

    handler =  agent_workflow.run(
 "Index the legacy code, generate parsed specification document, generate database schema,generate open api specificiation document, generate fastapi based rest api using parsed functional requirement document"
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