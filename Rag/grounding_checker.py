from Rag.llm import get_llm

from Rag.llm import get_llm


def is_answer_grounded(answer, documents):
    context = "\n\n".join(document.page_content for document in documents)

    prompt = f"""
Check whether the answer is fully supported by the document context.
Reply with only:
yes
or
no
Document context:
{context}
Answer:
{answer}
"""

    llm = get_llm()
    response = llm.invoke(prompt)
    result = response.content.strip().lower()

    return result == "yes"