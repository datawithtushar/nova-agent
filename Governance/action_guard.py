

# Action layer to determine free use or approval for required tools
def check_action(tool_name: str):
    safe_tools = [
        "read_subscriptions",
        "get_tasks",
        "create_chart",
        "create_docx_report",
        "create_pdf_report",
        "draft_email",
        "run_analysis",
    ]

    approval_tools = [
        "web_search",
        "update_subscriptions",
        "add_subscriptions",
        "create_task",
        "update_tasks",
        "send_email",
    ]

    if tool_name in safe_tools:
        return "allow"

    if tool_name in approval_tools:
        return "require_approval"

    return "block"