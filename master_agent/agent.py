from google.adk.agents.llm_agent import LlmAgent
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

root_agent = LlmAgent(
    name='root_agent',
    sub_agents=[procurement_agent, negotiation_agent],
    description='''A master agent that coordinates procurement and negotiation agents.''',
    tools=[approval_tool],
    instruction='''You are the master agent overseeing procurement and negotiation processes.
    Your task is to delegate tasks to the procurement_agent and negotiation_agent as needed.
    Use the external_approval_tool to get necessary approvals during the process.
    Ensure smooth coordination between the two agents to achieve the best outcomes for procurement and negotiation tasks.
    '''
)

