from Graph.router import plan_request

from Graph.context import (
    get_recent_messages,
    create_conversation_summary,
)


# --------------------------------------------------
# CONTEXT NODE
# --------------------------------------------------

def context_node(state):

    summary = create_conversation_summary(state)

    return {
        "conversation_summary": summary
    }


# --------------------------------------------------
# PLANNER / ROUTER NODE
# --------------------------------------------------

def router_node(state):

    recent_messages = get_recent_messages(state)

    recent_conversation = "\n".join(
        f"{message.type}: {message.content}"
        for message in recent_messages
    )

    summary = state.get(
        "conversation_summary",
        ""
    )

    conversation_context = f"""
Conversation summary:
{summary}

Recent conversation:
{recent_conversation}
"""

    plan = plan_request(
        state["question"],
        conversation_context
    )

    return {
        "execution_mode": plan["mode"],
        "selected_agents": plan["agents"]
    }