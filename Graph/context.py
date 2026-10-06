from Rag.llm import get_llm

# Context of last 6 messages
def get_recent_messages(state, limit=6):
    messages = state.get("messages", [])

    return messages[-limit:]

# Context summary of conversation
def create_conversation_summary(state, limit=6):

    messages = state.get("messages", [])

    # Short conversation -> no summary needed
    if len(messages) <= limit:
        return state.get("conversation_summary", "")

    previous_summary = state.get(
        "conversation_summary",
        ""
    )

    # Only summarize the older part
    old_messages = messages[:-limit]

    conversation = "\n".join(
        f"{message.type}: {message.content}"
        for message in old_messages
    )

    llm = get_llm()

    prompt = f"""
Update the conversation summary.

Previous summary:
{previous_summary}

Older conversation:
{conversation}

Create a concise updated summary.

Keep only useful context such as:
- important topics
- names
- decisions
- references
- user requests

Do not include unnecessary detail.
"""

    response = llm.invoke(prompt)

    return response.content.strip()