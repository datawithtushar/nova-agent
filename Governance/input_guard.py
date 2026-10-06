from Rag.llm import get_llm


def check_request(
    question: str,
    conversation: str = ""
):

    llm = get_llm()

    prompt = f"""
You are a security and scope guard for an enterprise AI assistant.

The assistant supports:

- normal conversation and greetings
- company document questions
- subscription management
- task management
- calculations and analysis
- charts and visualizations
- web research
- email drafting
- report generation

Conversation history may be provided.

IMPORTANT:

Allow normal conversational messages such as:
- hi
- hello
- thanks
- thank you
- okay
- what can you do?

Also allow short follow-up questions when they make sense from the conversation.

Examples:

Conversation:
User asked for a calculation.

Latest request:
"and divide that by 50"

Result:
allow


Conversation:
User discussed Statista subscription.

Latest request:
"when does it expire?"

Result:
allow


Return only one of:

allow
out_of_scope
unsafe

Use unsafe only for clearly harmful or destructive requests.

Use out_of_scope only when the request is clearly unrelated to the assistant's capabilities.

Conversation:
{conversation}

Latest request:
{question}
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()