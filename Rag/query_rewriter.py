from Rag.llm import get_llm


def rewrite_question(question):
    llm = get_llm()

    prompt = f"""
Rewrite the following question to improve document search.

Keep the original meaning.
Use clear keywords.
Return only the rewritten question.

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content.strip()