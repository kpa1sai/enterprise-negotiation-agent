import asyncio
import logging
from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.models.google_llm import Gemini
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

print(f"Procurement Agent - GOOGLE_CLOUD_PROJECT: {GOOGLE_CLOUD_PROJECT}, GOOGLE_CLOUD_LOCATION: {GOOGLE_CLOUD_LOCATION}")


from google.adk.a2a.utils.agent_to_a2a import to_a2a

logging.basicConfig( filename='procurement_agent.log',
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s")


def get_vendor_list():
    vendors = [
        {"name":"Office supplies Co", "products":["Paper", "Pens", "Notebooks"], "rating":4.5},
        {"name":"TechGear", "products":["Laptops", "Monitors", "Keyboards"], "rating":4.7},
        {"name":"Furniture World", "products":["Desks", "Chairs", "Cabinets"], "rating":4.3},
        {"name":"Stationery Hub", "products":["Envelopes", "Markers", "Folders"], "rating":4.6},
        {"name":"Zoho corp", "products":["Software licenses", "Cloud services"], "rating":4.8},
        {"name":"Catering Plus", "products":["Catering services", "Event supplies"], "rating":4.4},
        {"name":"Capgemini", "products":["Consulting services", "IT solutions"], "rating":4.2},
        {"name":"Cloudpivit", "products":["Consulting services", "IT solutions"], "rating":4.1},
    ]
    return vendors

def get_product_price_by_vendor(vendor_name: str, product_name: str):
    price_list = {
        "Office supplies Co": {"Paper": 5.0, "Pens": 2.0, "Notebooks": 3.5},
        "TechGear": {"Laptops": 800.0, "Monitors": 150.0, "Keyboards": 40.0},
        "Furniture World": {"Desks": 200.0, "Chairs": 100.0, "Cabinets": 150.0},
        "Stationery Hub": {"Envelopes": 1.0, "Markers": 2.5, "Folders": 3.0},
        "Zoho corp": {"Software licenses": 120.0, "Cloud services": 300.0},
        "Catering Plus": {"Catering services": 500.0, "Event supplies": 250.0},
        "Capgemini": {"Consulting services": 1000.0, "IT solutions": 2000.0},
        "Cloudpivit": {"Consulting services": 950.0, "IT solutions": 1800.0},
    }
    vendor_prices = price_list.get(vendor_name, {})
    return vendor_prices.get(product_name, None)

retry_config = types.HttpRetryOptions(
    attempts=3,
    initial_delay=1.0,
    max_delay=5.0,
    http_status_codes=[429, 500, 503, 504]
)

root_agent = Agent(
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    name='root_agent',
    description='A helpful assistant that gathers procurement requirements from business users.',
    instruction='''You are a procurement requirement gathering agent.
    Your task is to ask relevant questions to understand the procurement needs of the user and document them clearly. 
    Make sure to cover aspects such as budget, timeline, specifications, and any other pertinent details.
    Use get_vendor_list and get_product_price_by_vendor tools to assist in gathering information about vendors and product pricing as needed.
    If the requested item is present, You must provide the vendors, item price using the tools in a structured format to the user at the end of the conversation.
    If the item is not available, politely inform the user that the item is not available.
    ''',
    tools=[get_vendor_list, get_product_price_by_vendor],
)

APP_NAME = "procurement_agent"
USER_ID = "user_1234"
SESSION_ID = "session_5678"
session_service = InMemorySessionService()

async def init_session(app_name, user_id, session_id):
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    return session
session_1 = init_session(APP_NAME, USER_ID, SESSION_ID)
print(f"Session retrieved or created: {session_1}")

runner = Runner(
    agent = root_agent,
    app_name = APP_NAME,
    session_service = session_service
)

async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    print(f"Calling agent with query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    response = None

    async for event in runner.run_async(
        new_message=content,
        user_id=user_id,
        session_id=session_id
    ):
        print(f"Received event: {event}")
        if event.is_final_response() and event.content:
            parts = getattr(event.content, "parts", None)
            if parts and len(parts) > 0 and getattr(parts[0], "text", None) is not None:
                response = parts[0].text
                print(f"Agent response: {response}")
            else:
                print("Agent final response has no content parts or text.")
        elif event.actions and event.actions.escalate:
            print(f"Agent escalated : {event.actions.escalate or 'No reason provided'}")
            break
    if response is not None:
        return response
    else:
        raise Exception("No response received from agent.")

async def run_conversation():
    query = "What is the procurement process for office supplies?"
    await call_agent_async(query, runner, USER_ID, SESSION_ID)
    query = "Can you provide a list of approved vendors?"
    await call_agent_async(query, runner, USER_ID, SESSION_ID)

if __name__ == "__main__":
    try:
        asyncio.run(call_agent_async(query = "What's the weather in Tokyo?",
                        runner=runner,
                        user_id=USER_ID,
                        session_id=SESSION_ID))
    except Exception as e:
        print(f"An error occurred: {e}")


a2a_app = to_a2a(
    agent=root_agent,
    port=8080,
)