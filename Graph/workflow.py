from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

from Graph.state import AgentState

from Graph.governance_nodes import (
    input_guard_node,
    output_review_node,
)

from Graph.routing_nodes import (
    context_node,
    router_node,
)

from Graph.multi_agent import (
    multi_agent_executor_node,
)

from Database.conversation_db import (
    create_conversation,
    save_message,
)


# --------------------------------------------------
# DECISION FUNCTIONS
# --------------------------------------------------

def decide_after_guard(state):

    if state["guard_result"] == "allow":
        return "router"

    return "guard response"


def decide_after_review(state):

    if state["review_result"] == "pass":
        return "save answer"

    return "retry"


# --------------------------------------------------
# USER MESSAGE NODE
# --------------------------------------------------

def user_message_node(
    state,
    config
):

    thread_id = (
        config["configurable"]["thread_id"]
    )

    create_conversation(
        thread_id=thread_id,
        title=state["question"][:50]
    )

    save_message(
        thread_id=thread_id,
        role="user",
        content=state["question"]
    )

    return {
        "messages": [
            {
                "role": "user",
                "content": state["question"]
            }
        ]
    }


# --------------------------------------------------
# ASSISTANT MESSAGE NODE
# --------------------------------------------------

def assistant_message_node(
    state,
    config
):

    thread_id = (
        config["configurable"]["thread_id"]
    )

    save_message(
        thread_id=thread_id,
        role="assistant",
        content=state["answer"]
    )

    return {
        "messages": [
            {
                "role": "assistant",
                "content": state["answer"]
            }
        ]
    }


# --------------------------------------------------
# GUARD RESPONSE NODE
# --------------------------------------------------

def guard_response_node(state):

    result = state.get(
        "guard_result",
        ""
    )

    if result == "unsafe":

        answer = (
            "I can't help with that request."
        )

    else:

        answer = (
            "That request is outside the capabilities "
            "of this assistant."
        )

    return {
        "answer": answer
    }


# --------------------------------------------------
# RETRY NODE
# --------------------------------------------------

def retry_node(state):

    return {
        "answer": (
            "The previous answer did not pass "
            "the output review. Please try again."
        )
    }


# --------------------------------------------------
# CREATE GRAPH
# --------------------------------------------------

graph = StateGraph(
    AgentState
)


# --------------------------------------------------
# ADD NODES
# --------------------------------------------------

graph.add_node(
    "user message",
    user_message_node
)

graph.add_node(
    "context",
    context_node
)

graph.add_node(
    "input guard",
    input_guard_node
)

graph.add_node(
    "router",
    router_node
)

graph.add_node(
    "executor",
    multi_agent_executor_node
)

graph.add_node(
    "output reviewer",
    output_review_node
)

graph.add_node(
    "save answer",
    assistant_message_node
)

graph.add_node(
    "guard response",
    guard_response_node
)

graph.add_node(
    "retry",
    retry_node
)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

graph.set_entry_point(
    "user message"
)


# --------------------------------------------------
# USER MESSAGE -> CONTEXT
# --------------------------------------------------

graph.add_edge(
    "user message",
    "context"
)


# --------------------------------------------------
# CONTEXT -> INPUT GUARD
# --------------------------------------------------

graph.add_edge(
    "context",
    "input guard"
)


# --------------------------------------------------
# INPUT GUARD ROUTING
# --------------------------------------------------

graph.add_conditional_edges(
    "input guard",
    decide_after_guard,
    {
        "router": "router",
        "guard response": "guard response",
    }
)


# --------------------------------------------------
# GUARD RESPONSE -> SAVE ANSWER
# --------------------------------------------------

graph.add_edge(
    "guard response",
    "save answer"
)


# --------------------------------------------------
# ROUTER -> EXECUTOR
# --------------------------------------------------

graph.add_edge(
    "router",
    "executor"
)


# --------------------------------------------------
# EXECUTOR -> OUTPUT REVIEWER
# --------------------------------------------------

graph.add_edge(
    "executor",
    "output reviewer"
)


# --------------------------------------------------
# OUTPUT REVIEW ROUTING
# --------------------------------------------------

graph.add_conditional_edges(
    "output reviewer",
    decide_after_review,
    {
        "save answer": "save answer",
        "retry": "retry",
    }
)


# --------------------------------------------------
# RETRY -> SAVE ANSWER
# --------------------------------------------------

graph.add_edge(
    "retry",
    "save answer"
)


# --------------------------------------------------
# SAVE ANSWER -> END
# --------------------------------------------------

graph.add_edge(
    "save answer",
    END
)


# --------------------------------------------------
# MEMORY
# --------------------------------------------------

memory = InMemorySaver()


# --------------------------------------------------
# COMPILE
# --------------------------------------------------

app = graph.compile(
    checkpointer=memory
)