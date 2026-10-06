from Agents.general_agent import create_general_agent
from Agents.subscription_agent import create_subscription_agent
from Agents.analysis_agent import create_analysis_agent
from Agents.task_agent import create_task_agent
from Agents.web_agent import create_web_agent
from Agents.mail_agent import create_mail_agent
from Agents.visualization_agent import create_visualization_agent
from Agents.report_agent import create_report_agent

from Graph.rag_workflow import app as rag_app
from Graph.context import get_recent_messages


# --------------------------------------------------
# CREATE AGENT INSTANCES
# --------------------------------------------------

general_agent = create_general_agent()

subscription_agent = create_subscription_agent()

analysis_agent = create_analysis_agent()

task_agent = create_task_agent()

web_agent = create_web_agent()

mail_agent = create_mail_agent()

visualization_agent = create_visualization_agent()

report_agent = create_report_agent()


# --------------------------------------------------
# BUILD CONTEXT FOR AGENTS
# --------------------------------------------------

def build_agent_messages(state):

    recent_messages = get_recent_messages(
        state
    )

    summary = state.get(
        "conversation_summary",
        ""
    )

    messages = []


    if summary:

        messages.append(
            {
                "role": "system",
                "content": (
                    "Previous conversation summary:\n"
                    f"{summary}"
                )
            }
        )


    messages.extend(
        recent_messages
    )

    return messages


# --------------------------------------------------
# GENERAL AGENT
# --------------------------------------------------

def general_node(state):

    messages = build_agent_messages(
        state
    )

    result = general_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# SUBSCRIPTION AGENT
# --------------------------------------------------

def subscription_node(state):

    messages = build_agent_messages(
        state
    )

    result = subscription_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# ANALYSIS AGENT
# --------------------------------------------------

def analysis_node(state):

    messages = build_agent_messages(
        state
    )

    result = analysis_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# TASK AGENT
# --------------------------------------------------

def task_node(state):

    messages = build_agent_messages(
        state
    )

    result = task_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# WEB AGENT
# --------------------------------------------------

def web_node(state):

    messages = build_agent_messages(
        state
    )

    result = web_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# MAIL AGENT
# --------------------------------------------------

def mail_node(state):

    messages = build_agent_messages(
        state
    )

    result = mail_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# VISUALIZATION AGENT
# --------------------------------------------------

def visualization_node(state):

    messages = build_agent_messages(
        state
    )

    result = visualization_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# REPORT AGENT
# --------------------------------------------------

def report_node(state):

    messages = build_agent_messages(
        state
    )

    result = report_agent.invoke({
        "messages": messages
    })

    return {
        "answer":
        result["messages"][-1].content
    }


# --------------------------------------------------
# RAG AGENT
# --------------------------------------------------

def rag_node(state):

    recent_messages = get_recent_messages(
        state
    )

    summary = state.get(
        "conversation_summary",
        ""
    )


    recent_conversation = "\n".join(
        f"{message.type}: {message.content}"
        for message in recent_messages
    )


    rag_question = f"""
Use the conversation context to understand the latest question.

Conversation summary:
{summary}

Recent conversation:
{recent_conversation}

Latest user question:
{state["question"]}
"""


    result = rag_app.invoke({
        "question": rag_question,
        "retry_count": 0
    })


    return {
        "answer": result["answer"],
        "sources": result.get(
            "sources",
            []
        )
    }