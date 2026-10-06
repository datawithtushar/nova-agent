from langchain.agents import create_agent
from Rag.llm import get_llm
from Tools.task_tool import create_task, get_tasks, update_tasks


def create_task_agent():
    agent=create_agent(
        model=get_llm(),
        tools=[create_task, get_tasks, update_tasks],
        system_prompt="""
        You are a task management agent.

        You can:
        - create tasks
        - view tasks
        - update one or more tasks

        Use the available tools whenever the user asks about task data.""")
    
    return agent