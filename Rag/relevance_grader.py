from Rag.llm import get_llm


# Implementing corrective rag by retrieving relevant documents and asking the LLM to determine relevance--------

def is_relevant(question, document):
    """Determine if a document is relevant to a given question using the LLM."""
    llm = get_llm()
    prompt = f"""
Check whether the document content is relevant to the user's question.

Reply with only:
yes
or
no

Question:
{question}

Document content:
{document.page_content}
"""
    
    response= llm.invoke(prompt)
    result = response.content.strip().lower()

    return result == "yes"


# Filtering relevant documents and displaying their content-------------------------------------------------------------

def filter_relevant_documents(question, documents):
    """Filter and return only the relevant documents based on the question."""
    relevant_docs = []

    for document in documents:
        if is_relevant(question, document):
            relevant_docs.append(document)

    return relevant_docs
