from concurrent.futures import ThreadPoolExecutor

from Graph.agent_nodes import (
    general_node,
    rag_node,
    subscription_node,
    analysis_node,
    task_node,
    web_node,
    mail_node,
    visualization_node,
    report_node,
)


# --------------------------------------------------
# AGENT REGISTRY
# --------------------------------------------------

AGENTS = {
    "general": general_node,
    "rag": rag_node,
    "subscription": subscription_node,
    "analysis": analysis_node,
    "task": task_node,
    "web": web_node,
    "mail": mail_node,
    "visualization": visualization_node,
    "report": report_node,
}


# --------------------------------------------------
# RUN ONE AGENT
# --------------------------------------------------

def run_agent(agent_name, state):

    agent_function = AGENTS[agent_name]

    return agent_function(state)


# --------------------------------------------------
# SINGLE MODE
# --------------------------------------------------

def run_single(state, agents):

    agent_name = agents[0]

    result = run_agent(
        agent_name,
        state
    )

    return {
        "answer": result["answer"],
        "agent_results": {
            agent_name: result["answer"]
        },
        "sources": result.get("sources", [])
    }


# --------------------------------------------------
# PARALLEL MODE
# --------------------------------------------------

def run_parallel(state, agents):

    results = {}

    sources = []

    with ThreadPoolExecutor(
        max_workers=len(agents)
    ) as executor:

        futures = {
            agent_name: executor.submit(
                run_agent,
                agent_name,
                state
            )
            for agent_name in agents
        }

        for agent_name, future in futures.items():

            result = future.result()

            results[agent_name] = result["answer"]

            if result.get("sources"):
                sources.extend(
                    result["sources"]
                )

    combined_answer = "\n\n".join(
        f"{agent_name.upper()} AGENT:\n{answer}"
        for agent_name, answer in results.items()
    )

    return {
        "answer": combined_answer,
        "agent_results": results,
        "sources": sources
    }


# --------------------------------------------------
# SEQUENTIAL MODE
# --------------------------------------------------

def run_sequential(state, agents):

    results = {}

    sources = []

    working_state = dict(state)

    previous_results = ""

    for agent_name in agents:

        # Give later agents results from earlier agents
        if previous_results:

            existing_summary = working_state.get(
                "conversation_summary",
                ""
            )

            working_state[
                "conversation_summary"
            ] = f"""
{existing_summary}

Previous agent results:
{previous_results}
"""

        result = run_agent(
            agent_name,
            working_state
        )

        answer = result["answer"]

        results[agent_name] = answer

        if result.get("sources"):
            sources.extend(
                result["sources"]
            )

        previous_results += (
            f"\n{agent_name.upper()} AGENT:\n"
            f"{answer}\n"
        )

    # Final agent gives final answer
    final_agent = agents[-1]

    final_answer = results[
        final_agent
    ]

    return {
        "answer": final_answer,
        "agent_results": results,
        "sources": sources
    }


# --------------------------------------------------
# MAIN EXECUTOR NODE
# --------------------------------------------------

def multi_agent_executor_node(state):

    mode = state.get(
        "execution_mode",
        "single"
    )

    agents = state.get(
        "selected_agents",
        []
    )

    if not agents:

        return {
            "answer": (
                "No suitable agent was selected."
            )
        }

    if mode == "parallel":

        return run_parallel(
            state,
            agents
        )

    if mode == "sequential":

        return run_sequential(
            state,
            agents
        )

    return run_single(
        state,
        agents
    )