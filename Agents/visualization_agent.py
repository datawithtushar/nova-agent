from langchain.agents import create_agent
from Rag.llm import get_llm
from Tools.visualization_tool import create_chart


def create_visualization_agent():
    agent = create_agent(
        model=get_llm(),
        tools=[create_chart],
        system_prompt="""
        You are a visualization agent.

        Use the chart tool whenever the user asks for a chart
        or visual comparison.

        Choose the most suitable chart type:
        - bar
        - line
        - pie
        - scatter
        """
    )

    return agent