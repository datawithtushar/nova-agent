import json

from Rag.llm import get_llm


AVAILABLE_AGENTS = [
    "general",
    "rag",
    "analysis",
    "subscription",
    "task",
    "visualization",
    "mail",
    "web",
    "report",
]


def plan_request(
    question: str,
    conversation: str = ""
):

    llm = get_llm()

    prompt = f"""
You are the planner for a multi-agent enterprise assistant.

Available agents:

general
- Greetings
- Thanks
- Normal conversation
- Asking what the assistant can do
- Simple acknowledgements

rag
- Questions about company documents
- Internal knowledge
- Document-based questions

analysis
- Calculations
- Percentages
- Averages
- Ratios
- Numeric analysis

subscription
- Read subscription data
- Add subscriptions
- Update subscriptions

task
- Create tasks
- View tasks
- Update tasks

visualization
- Charts
- Visual comparisons

mail
- Draft professional emails

web
- Current information
- External information
- Web research

report
- PDF and Word reports


Choose which agent or agents are needed.

Choose one execution mode:

single
- one agent is enough

parallel
- multiple agents can work independently

sequential
- later agents depend on earlier agent results


IMPORTANT:

Use conversation history when understanding short follow-up questions.

Examples:

"Hi"

{{
    "mode": "single",
    "agents": ["general"]
}}


"Thanks"

{{
    "mode": "single",
    "agents": ["general"]
}}


"What can you do?"

{{
    "mode": "single",
    "agents": ["general"]
}}


"What is 20 times 10?"

{{
    "mode": "single",
    "agents": ["analysis"]
}}


Conversation:
User: What is 20 times 10?
Assistant: 20 × 10 = 200

Latest request:
"And divide that by 50"

{{
    "mode": "single",
    "agents": ["analysis"]
}}


"Show my subscriptions and find the latest GBP/USD rate"

{{
    "mode": "parallel",
    "agents": ["subscription", "web"]
}}


"Read the contract and draft an email"

{{
    "mode": "sequential",
    "agents": ["rag", "mail"]
}}


"Get the latest exchange rate and use it to convert my subscription costs"

{{
    "mode": "sequential",
    "agents": ["subscription", "web", "analysis"]
}}


Return ONLY valid JSON.

Conversation:
{conversation}

Latest request:
{question}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    try:

        plan = json.loads(
            content
        )

    except json.JSONDecodeError:

        return {
            "mode": "single",
            "agents": ["general"]
        }


    mode = plan.get(
        "mode",
        "single"
    )

    agents = plan.get(
        "agents",
        []
    )


    agents = [
        agent
        for agent in agents
        if agent in AVAILABLE_AGENTS
    ]


    if not agents:

        agents = [
            "general"
        ]


    if mode not in [
        "single",
        "parallel",
        "sequential"
    ]:

        mode = "single"


    if mode == "single":

        agents = [
            agents[0]
        ]


    return {
        "mode": mode,
        "agents": agents
    }