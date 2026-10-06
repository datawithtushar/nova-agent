from langgraph.graph import END, StateGraph
from Graph.state import AgentState
from Graph.rag_nodes import (
    retrieve_node,
    grade_documents_node,
    generate_answer_node,
    grounding_check_node,
    rewrite_question,
    decide_after_grading,
    not_found_node
)


# Creating the graph workflow (Nodes, entry, edge)
def create_graph():

    graph=StateGraph(AgentState)

    graph.add_node("retrieve",retrieve_node)
    graph.add_node("grade",grade_documents_node)
    graph.add_node("answer",generate_answer_node)
    graph.add_node("verify answer",grounding_check_node)
    graph.add_node("rewrite query",rewrite_question)
    graph.add_node("Not found",not_found_node)


    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges("grade",decide_after_grading,
    {
        "generate answer": "answer",
        "rewrite question": "rewrite query",
        "not found": "Not found",},)
    
    graph.add_edge("answer", "verify answer")
    graph.add_edge("verify answer", END)
    graph.add_edge("rewrite query", "retrieve")
    graph.add_edge("Not found",END)

    return graph.compile()

app = create_graph()




