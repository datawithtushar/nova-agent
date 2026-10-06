from langgraph.types import interrupt

# Human in the Loop for Approval
def request_approval(action_description: str):
    decision = interrupt(
        {
            "message": "Approval required",
            "action": action_description
        }
    )

    return decision