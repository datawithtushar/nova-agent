from langchain.agents import create_agent
from Rag.llm import get_llm
from Tools.mail_tool import draft_email, send_email


def create_mail_agent():
    agent = create_agent(
        model=get_llm(),
        tools=[draft_email,send_email,],
        system_prompt="""
        You are a professional email assistant.

        Your job is to:
        - write clear and professional emails
        - use the information provided by the user or other agents
        - create a draft first
        - never send an email unless the user has explicitly approved it

        If important information is missing, ask the user for it.
        """
    )

    return agent