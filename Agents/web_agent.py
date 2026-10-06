from langchain.agents import create_agent
from Rag.llm import get_llm
from Tools.web_search_tool import web_search


def create_web_agent():
    agent = create_agent(
        model=get_llm(),
        tools=[web_search],
        system_prompt="""
        You are a web research agent.

        When the user asks for current, recent, live, or external
        information, use the web_search tool.

        Call web_search using a concise search query.

        After receiving search results, answer the user's question
        using the retrieved information.

        Do not invent current information if the web_search tool
        has not been used.
        """
    )

    return agent