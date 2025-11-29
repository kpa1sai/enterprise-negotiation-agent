from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners.runner import Runner
from google.genai import types

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

session_service = InMemorySessionService()

APP_NAME = "procurement_agent"
USER_ID = "user_1234"
SESSION_ID = "session_5678"

session = await session_service.get_or_create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session retrieved or created: {session}")

runner = Runner(
    agent = procurement_agent,
    app_name = APP_NAME,
    session_service = session_service
)

async def call_agent_async(query: str, runner, user_id: str, session_id: str):
    response = await runner.run(
        input=types.TextInput(text=query),
        user_id=user_id,
        session_id=session_id
    )
    return response