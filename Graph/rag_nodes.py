from Rag.retriever import retrieve_documents
from Rag.relevance_grader import filter_relevant_documents
from Rag.query_rewriter import rewrite_question
from Rag.grounding_checker import is_answer_grounded
from Rag.llm import get_llm
from Governance.input_guard import check_request



# Retriving nodes of our graph
def retrieve_node(state):

    question= state.get("rewritten_question",state["question"])
    documents=retrieve_documents(question)

    return {"documents":documents}


# Grading Node for retrived documents
def grade_documents_node(state):

    question=state["question"]
    documents=state["documents"]
    relevant_documents=filter_relevant_documents(question,documents)

    return {"relevant_documents":relevant_documents}


# Deciding after grading node-------------------------------------------------------
def decide_after_grading(state):
    relevant_documents=state["relevant_documents"]
    retry_count=state.get("retry_count",0)

    if relevant_documents:
        return "generate answer"
    
    if retry_count>=1:
        return "not found"
    
    return "rewrite question"


# Rewritting question node
def rewrite_question(state):
    question=state["question"]
    rewritten_question=rewrite_question(question)

    retry_count=state.get("retry_count",0)+1

    return {"rewritten_question":rewritten_question,
            "retry_count":retry_count}


# Not found node
def not_found_node(state):
    return {
        "answer": (
            "I could not find this information "
            "in the available documents."
        ),
        "sources": []
    }


# Generate Answer node
def generate_answer_node(state):
    question = state["question"]
    documents = state["relevant_documents"]

    context = "\n\n".join(document.page_content for document in documents)

    prompt = f"""
Answer the question only from the context below.

Context:
{context}

Question:
{question}
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return {"answer": response.content}


# Checking the result/answer
def grounding_check_node(state):

    answer = state["answer"]
    documents = state["relevant_documents"]
    grounded = is_answer_grounded(answer,documents,)

    if grounded == "no":
        return {
            "answer": (
                "I could not generate a fully supported answer "
                "from the available documents."
            ),
            "grounded": grounded
        }

    return {"grounded": grounded}
