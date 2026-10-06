from Governance.input_guard import check_request
from Governance.action_guard import check_action
from Governance.human_approval import request_approval
from Governance.output_reviewer import review_output



# Input guard node
def input_guard_node(state):

    question = state["question"]

    summary = state.get(
        "conversation_summary",
        ""
    )

    recent_messages = state.get(
        "messages",
        []
    )[-6:]

    recent_conversation = "\n".join(
        f"{message.type}: {message.content}"
        for message in recent_messages
    )

    conversation = f"""
Conversation summary:
{summary}

Recent conversation:
{recent_conversation}
"""

    result = check_request(
        question,
        conversation
    )

    return {
        "guard_result": result
    }

# Reviewing output node
def output_review_node(state):

    result = review_output(
        question=state["question"],
        answer=state["answer"]
    )

    return {
        "review_result": result["status"],
        "answer": result["answer"]
    }



# Action guard node for tool 
def action_guard_node(state):
    tool_name = state["tool_name"]
    result = check_action(tool_name)

    return {"action_result": result}


# Node for Approval based on tool type
def approval_node(state):
    decision = request_approval(
        f"Allow tool '{state['tool_name']}' to run?")

    return {"approval": decision}

# Blocked Node
def blocked_node(state):
    return {"answer": "This action is not allowed."}
