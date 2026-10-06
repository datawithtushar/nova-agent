from pydantic_settings import sources
from Rag.retriever import retrieve_documents
from Rag.relevance_grader import filter_relevant_documents  
from Rag.query_rewriter import rewrite_question
from Rag.llm import get_llm
from Rag.grounding_checker import is_answer_grounded


# Asking questions and getting responses based on context-------------------------------------------------------------

def start_question(question):

    documents = retrieve_documents(question)
    relevant_documents = filter_relevant_documents(question, documents)


    # Retry once with a rewritten question
    if not relevant_documents:
        rewritten_question = rewrite_question(question)

        documents = retrieve_documents(rewritten_question)

        relevant_documents = filter_relevant_documents(rewritten_question, documents)

    if not relevant_documents:
        return ("I could not find any relevant information in the available documents.", [])

    context = "\n\n".join([doc.page_content for doc in relevant_documents])

    prompt=f"""
You are a company policy assistant.
Answer the question only from the context below.
If the answer is not available in the context, say:
"I could not find this information in the available documents."

Context:{context}
Question: {question}"""
    
    llm = get_llm()
    response = llm.invoke(prompt)

    answer = response.content
    if not is_answer_grounded(answer, relevant_documents):
          return ("I could not generate a fully supported answer from the available documents.",[],)


# Extracting sources for the retrieved documents-----

    sources = []

    for document in relevant_documents:
        file_name = document.metadata.get("file_name", "Unknown file")
        page = document.metadata.get("page")

        if page is not None:
            source = f"{file_name}, page {page + 1}"
        else:
            source = file_name

        if source not in sources:
            sources.append(source)

    return answer, sources



