from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.function_tool import FunctionTool
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
import asyncio
import logging
import dotenv
import os

dotenv.load_dotenv()
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

print(f"Master Agent - GOOGLE_CLOUD_PROJECT: {GOOGLE_CLOUD_PROJECT}, GOOGLE_CLOUD_LOCATION: {GOOGLE_CLOUD_LOCATION}")

logging.basicConfig( filename='log/master_agent.log',
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s")

async def external_approval_tool():
    '''A tool to simulate external approval process.'''
    print(f"External approval tool invoked by master_agent.")
    await asyncio.sleep(10)  # Simulate some processing delay
    return {"approval_status":"approved"}

approval_tool = FunctionTool(func=external_approval_tool)



procurement_agent = RemoteA2aAgent(
    name='procurement_agent',
    agent_card= "http://localhost:8080",
    description='A remote agent handling procurement tasks.'
)

root_agent = LlmAgent(
    name='master_agent',
    model='gemini-2.5-flash',
    sub_agents=[procurement_agent],
    description='''A master agent that coordinates procurement agent and approval tool.''',
    tools=[approval_tool],
    instruction='''You are the master agent overseeing procurement processes.
    Your task is to delegate tasks to the procurement_agent as needed.
    Use the approval_tool to get necessary approvals after the procurement agent tasks are completed.
    Ensure smooth coordination between the two agents to achieve the best outcomes for procurement and negotiation tasks.
    '''
)


