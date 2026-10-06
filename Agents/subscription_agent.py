from langchain.agents import create_agent
from Rag.llm import get_llm
from Tools.google_sheets import read_subscriptions,update_subscriptions,add_subscriptions

#Subscription Agent Creation
def create_subscription_agent():
    agent = create_agent(
        model=get_llm(),
        tools=[
            read_subscriptions,
            update_subscriptions,
            add_subscriptions,
        ],
        system_prompt="""
        You are a subscription management agent.

        You can:
        - read subscription records
        - update existing subscriptions
        - add new subscriptions

        Use the available tools whenever the user asks about
        subscription tracker data.

        If required information is missing for adding a new subscription,
        ask the user for the missing details before using the tool.
        """
    )

    return agent