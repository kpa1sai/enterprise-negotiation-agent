from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.loop_agent import LoopAgent
from ..procurement_agent.agent import root_agent as procurement_agent
from ..negotitation_agent.agent import root_agent as negotiation_agent
from google.adk.tools.function_tool import FunctionTool
import asyncio

async def external_approval_tool():
    '''A tool to simulate external approval process.'''
    print(f"External approval tool invoked by master_agent.")
    await asyncio.sleep(10)  # Simulate some processing delay
    return {"approval_status":"approved"}

approval_tool = FunctionTool(func=external_approval_tool)

root_agent = SequentialAgent(
    name='root_agent',
    sub_agents=[procurement_agent, negotiation_agent],
    description='''A master agent that coordinates procurement and negotiation agents.''',
)

