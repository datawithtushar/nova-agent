from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


# Creating a memory with state for our flow

class AgentState(TypedDict, total=False):
    # User input & output
    question: str
    answer: str

    # Message history
    messages: Annotated[list, add_messages]
    conversation_summary: str

    # Routing
    selected_agent: str

    # Governance
    tool_name: str
    guard_result: str
    review_result: str
    action_result: str
    approval: str

    # Parallel & Sequential execution
    execution_mode: str
    selected_agents: list
    agent_results: dict

    # RAG fields
    rewritten_question: str
    documents: list
    relevant_documents: list
    sources: list
    retry_count: int
    grounded: str

    

