from langchain.agents import create_agent
from Rag.llm import get_llm
from Tools.report_tool import create_docx_report,create_pdf_report


def create_report_agent():
    agent = create_agent(
        model=get_llm(),
        tools=[create_docx_report,create_pdf_report],
        system_prompt="""
        You are a report generation agent.

        Create professional reports using information provided
        by the user or other agents.

        Choose the correct tool based on the requested format:
        - Word / DOCX -> create_docx_report
        - PDF -> create_pdf_report

        Create a clear title and well-structured content before
        generating the file.
        """
    )

    return agent