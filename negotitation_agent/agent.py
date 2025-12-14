from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.loop_agent import LoopAgent
import logging


logging.basicConfig( filename='negotiation_agent.log',
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s")

def get_vendor_contact_info(vendor_name: str):
    contact_info = [{"name":"Office supplies Co", "contact":"office@officesuppliesco.com"},
                    {"name":"Stationery World", "contact":"stationery@stationeryworld.com"},
                    {"name":"TechGear", "contact":"techgear@techgear.com"},
                    {"name":"Furniture Hub", "contact":"furniture@furniturehub.com"},
                    {"name":"Zoho corp", "contact":"contact@zohocorp.com"},
                    {"name":"Catering Plus", "contact":"info@cateringplus.com"},
                    {"name":"Capgemini", "contact":"support@capgemini.com"},
                    {"name":"Cloudpivit", "contact":"hello@cloudpivit.com"},
                    ]
    for vendor in contact_info:
        if vendor["name"] == vendor_name:
            return vendor["contact"]
    return None

def exit_refinement_loop():
    '''Function to exit the refinement loop.'''
    print(f"Exiting the refinement loop by refinement_agent.")
    return {}


def send_negotiation_email(vendor_name: str, subject: str, body: str):
    contact = get_vendor_contact_info(vendor_name)
    if contact:
        # Simulate sending email
        return f"Email sent to {contact} with subject '{subject}' and body '{body}'."
    else:
        return f"Vendor {vendor_name} not found."


initial_draft_agent = Agent(
    model='gemini-2.5-flash',
    name='initial_draft_agent',
    description='An agent that drafts initial negotiation emails based on procurement requirements.',
    instruction='''You are an initial draft agent.
    Your task is to draft negotiation emails to vendors based on the procurement requirements provided.
    Make sure to address key points such as pricing, delivery timelines, and payment terms.
    If the product or service is available with existing vendors, Create an initial draft email to start negotiating with the vendors.
    Use get_vendor_contact_info for gathering vendor details.
    ''',
    tools=[get_vendor_contact_info]
)

critique_agent = Agent(
    model='gemini-2.5-flash',
    name='critique_agent',
    description='An agent that critiques and provides feedback on negotiation strategies and email drafts.',
    instruction='''You are a constructive critique for helping draft creative emails to negotiate with vendors.
    The email should use industry standard negotiating tactics to get a best deal from the vendors.
    If you find the email professional and following all the previous rules, invoke exit_refinement_loop tool.
    Otherwise, give all the improvements that can be made to the email.''',
    tools=[exit_refinement_loop]
)

refinement_agent = Agent(
    model='gemini-2.5-flash',
    name='refinement_agent',
    description='An agent that refines and improves negotiation email drafts based on critique feedback.',
    instruction='''You are a refinement agent.
    Your task is to refine and improve negotiation email drafts based on the feedback provided by the critique agent.
    Make sure to incorporate all the suggestions and enhance the clarity, tone, and effectiveness of the email.
    ''',
)

refinement_loop = LoopAgent(
    name='refinement_loop',\
    sub_agents=[critique_agent, refinement_agent],
    max_iterations=2,
    description='An agent that engages in multi-turn refinement of negotiation email drafts.'
)

root_agent = SequentialAgent(
    name='root_agent',
    sub_agents=[initial_draft_agent, refinement_loop],
    description='''A master agent that coordinates negotiation email drafting and refinement agents.''',
)