from Graph.workflow import app
from Database.conversation_db import get_messages


def run_chat(question: str, thread_id: str):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    snapshot = app.get_state(config)

    input_state = {
        "question": question
    }

    # Restore previous conversation from SQLite
    # only when LangGraph does not already have it
    if not snapshot.values.get("messages"):

        old_messages = get_messages(thread_id)

        if old_messages:

            input_state["messages"] = [
                {
                    "role": role,
                    "content": content
                }
                for (
                    message_id,
                    role,
                    content,
                    created_at
                ) in old_messages
            ]

    result = app.invoke(
        input_state,
        config=config
    )

    return result