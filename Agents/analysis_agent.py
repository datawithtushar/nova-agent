from langchain.agents import create_agent
from Tools.analysis_tool import run_analysis
from Rag.llm import get_llm


# Analysis Agent Creation
def create_analysis_agent():

    Agent=create_agent(
        model=get_llm(),
        tools=[run_analysis],
        system_prompt="""You are an analysis agent.
        Use the analysis tool whenever calculations are required.
        Do not calculate values yourself when the tool can perform them.""")
    
    return Agent