import os
import uuid

import requests
import streamlit as st


# --------------------------------------------------
# FASTAPI CONFIG
# --------------------------------------------------

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Nova",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SIMPLE UI STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.4rem;
    }

    div[data-testid="stChatInput"] {
        border-radius: 14px;
    }

    .footer-text {
        text-align: center;
        color: #737373;
        font-size: 0.78rem;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# API HELPER FUNCTIONS
# --------------------------------------------------

def get_conversations():

    try:

        response = requests.get(
            f"{API_URL}/conversations",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return []


def get_messages(thread_id):

    try:

        response = requests.get(
            f"{API_URL}/conversations/{thread_id}",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return []


def send_feedback(
    thread_id,
    message_id,
    feedback
):

    response = requests.post(
        f"{API_URL}/feedback",
        json={
            "thread_id": thread_id,
            "message_id": message_id,
            "feedback": feedback
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def remove_conversation(thread_id):

    response = requests.delete(
        f"{API_URL}/conversations/{thread_id}",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "thread_id" not in st.session_state:

    st.session_state.thread_id = str(
        uuid.uuid4()
    )


if "last_result" not in st.session_state:

    st.session_state.last_result = None


if "is_processing" not in st.session_state:

    st.session_state.is_processing = False


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title(
        "✨ Nova"
    )

    st.caption(
        "Networked Orchestrated Virtual Assistant"
    )

    st.caption(
        "Agentic AI workspace for knowledge, "
        "analysis, research and connected tools."
    )

    st.divider()


    # ----------------------------------------------
    # CONTRIBUTORS
    # ----------------------------------------------

    st.subheader(
        "Contributors"
    )

    st.write(
        "Tushar and Team"
    )

    st.caption(
        "Built as an end-to-end multi-agent AI project."
    )

    st.divider()


    # ----------------------------------------------
    # NEW CHAT
    # ----------------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True,
        type="primary",
        disabled=st.session_state.is_processing
    ):

        st.session_state.thread_id = str(
            uuid.uuid4()
        )

        st.session_state.last_result = None

        st.rerun()


    if st.session_state.is_processing:

        st.caption(
            "Nova is currently processing a request."
        )


    # ----------------------------------------------
    # CHAT HISTORY
    # ----------------------------------------------

    st.subheader(
        "Chat History"
    )

    conversations = get_conversations()


    if conversations:

        for conversation in conversations:

            saved_thread_id = conversation.get(
                "thread_id"
            )

            title = conversation.get(
                "title"
            )

            chat_col, delete_col = st.columns(
                [0.84, 0.16]
            )


            with chat_col:

                if st.button(
                    title or "New Chat",
                    key=f"chat_{saved_thread_id}",
                    use_container_width=True,
                    disabled=st.session_state.is_processing
                ):

                    st.session_state.thread_id = (
                        saved_thread_id
                    )

                    st.session_state.last_result = None

                    st.rerun()


            with delete_col:

                if st.button(
                    "✕",
                    key=f"delete_{saved_thread_id}",
                    help="Delete conversation",
                    disabled=st.session_state.is_processing
                ):

                    try:

                        remove_conversation(
                            saved_thread_id
                        )

                        if (
                            st.session_state.thread_id
                            == saved_thread_id
                        ):

                            st.session_state.thread_id = str(
                                uuid.uuid4()
                            )

                            st.session_state.last_result = None

                        st.rerun()


                    except Exception:

                        st.error(
                            "Unable to delete the conversation "
                            "at the moment."
                        )

    else:

        st.caption(
            "Your previous conversations will appear here."
        )


    st.divider()


    # ----------------------------------------------
    # CAPABILITIES
    # ----------------------------------------------

    with st.expander(
        "What can Nova do?"
    ):

        st.markdown(
            """
            - Search internal documents
            - Perform calculations and analysis
            - Manage subscription information
            - Work with tasks
            - Research current information
            - Draft emails
            - Generate reports
            - Create visualisations
            - Coordinate multiple specialist agents
            """
        )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="main-title">
        How can I help you today?
    </div>

    <div class="main-subtitle">
        Nova can coordinate specialist agents, tools and knowledge
        sources to handle simple and complex requests.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIMPLE INTRODUCTION
# --------------------------------------------------

st.subheader(
    "Nova Workspace"
)

st.write(
    "Nova is a multi-agent AI workspace designed to work with enterprise "
    "documents, calculations, subscriptions, tasks, live web research and "
    "connected tools. Complex requests can be handled by multiple specialist "
    "agents automatically."
)


# --------------------------------------------------
# CURRENT CONVERSATION
# --------------------------------------------------

thread_id = st.session_state.thread_id

history = get_messages(
    thread_id
)


# --------------------------------------------------
# EMPTY CHAT STATE
# --------------------------------------------------

if not history:

    st.markdown(
        "#### Try asking"
    )

    example_col1, example_col2, example_col3 = st.columns(
        3
    )


    with example_col1:

        st.info(
            "📄 Ask a question about available documents."
        )


    with example_col2:

        st.info(
            "📊 Analyse data or perform a calculation."
        )


    with example_col3:

        st.info(
            "🌐 Research the latest external information."
        )


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in history:

    message_id = message.get(
        "message_id"
    )

    role = message.get(
        "role"
    )

    content = message.get(
        "content",
        ""
    )


    if role == "user":

        with st.chat_message(
            "user"
        ):

            st.markdown(
                content
            )


    elif role == "assistant":

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                content
            )


            positive_col, negative_col, _ = st.columns(
                [0.055, 0.055, 0.89]
            )


            with positive_col:

                if st.button(
                    "👍",
                    key=f"positive_{message_id}",
                    help="Helpful response",
                    disabled=st.session_state.is_processing
                ):

                    try:

                        send_feedback(
                            thread_id=thread_id,
                            message_id=message_id,
                            feedback="positive"
                        )

                        st.toast(
                            "Thanks for the feedback!"
                        )

                    except Exception:

                        st.error(
                            "Unable to save feedback "
                            "at the moment."
                        )


            with negative_col:

                if st.button(
                    "👎",
                    key=f"negative_{message_id}",
                    help="Not helpful",
                    disabled=st.session_state.is_processing
                ):

                    try:

                        send_feedback(
                            thread_id=thread_id,
                            message_id=message_id,
                            feedback="negative"
                        )

                        st.toast(
                            "Feedback saved."
                        )

                    except Exception:

                        st.error(
                            "Unable to save feedback "
                            "at the moment."
                        )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

prompt = st.chat_input(
    "Message Nova...",
    accept_file="multiple",
    file_type=[
        "png",
        "jpg",
        "jpeg"
    ],
    accept_audio=True,
    disabled=st.session_state.is_processing
)


# --------------------------------------------------
# HANDLE NEW INPUT
# --------------------------------------------------

if prompt:

    question = prompt.text

    uploaded_files = prompt.files

    audio_file = prompt.audio


    # ----------------------------------------------
    # IMAGE PREVIEW
    # ----------------------------------------------

    if uploaded_files:

        for uploaded_file in uploaded_files:

            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                width=250
            )


    # ----------------------------------------------
    # AUDIO PREVIEW
    # ----------------------------------------------

    if audio_file:

        st.audio(
            audio_file
        )


    # ----------------------------------------------
    # PROCESS MESSAGE
    # ----------------------------------------------

    if question:

        st.session_state.is_processing = True


        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )


        with st.chat_message(
            "assistant"
        ):

            try:

                with st.status(
                    "Nova is processing your request...",
                    expanded=True
                ) as status:

                    status.write(
                        "Understanding the request..."
                    )


                    # ----------------------------------
                    # CALL FASTAPI
                    # ----------------------------------

                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "question": question,
                            "thread_id": thread_id
                        },
                        timeout=180
                    )


                    status.write(
                        "Running the selected agent workflow..."
                    )


                    response.raise_for_status()


                    result = response.json()


                    status.write(
                        "Preparing the final response..."
                    )


                    answer = result.get(
                        "answer",
                        "Nova was unable to generate a response."
                    )


                    status.update(
                        label="Completed",
                        state="complete",
                        expanded=False
                    )


                st.markdown(
                    answer
                )


                st.session_state.last_result = (
                    result
                )


                st.session_state.is_processing = False


                st.rerun()


            # ------------------------------------------
            # BACKEND NOT REACHABLE
            # ------------------------------------------

            except requests.exceptions.ConnectionError:

                st.session_state.is_processing = False

                st.error(
                    "Nova is temporarily unavailable. "
                    "Please try again in a moment."
                )


            # ------------------------------------------
            # TIMEOUT
            # ------------------------------------------

            except requests.exceptions.Timeout:

                st.session_state.is_processing = False

                st.error(
                    "This request is taking longer than expected. "
                    "Please try again."
                )


            # ------------------------------------------
            # BACKEND ERROR
            # ------------------------------------------

            except requests.exceptions.HTTPError:

                st.session_state.is_processing = False

                st.error(
                    "Nova was unable to complete the request. "
                    "Please try again in a moment."
                )


            # ------------------------------------------
            # UNKNOWN ERROR
            # ------------------------------------------

            except Exception:

                st.session_state.is_processing = False

                st.error(
                    "Something went wrong while processing your request. "
                    "Please try again."
                )


# --------------------------------------------------
# AGENT DETAILS
# --------------------------------------------------

result = st.session_state.last_result


if result:

    with st.expander(
        "⚙️ Agent activity"
    ):

        execution_mode = result.get(
            "execution_mode",
            "single"
        )

        selected_agents = result.get(
            "selected_agents",
            []
        )


        detail_col1, detail_col2 = st.columns(
            2
        )


        with detail_col1:

            st.metric(
                "Execution Mode",
                execution_mode.title()
            )


        with detail_col2:

            st.write(
                "**Specialist Agents**"
            )


            if selected_agents:

                for agent in selected_agents:

                    st.write(
                        f"• {agent.title()}"
                    )

            else:

                st.write(
                    "• General"
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer-text">
        Nova • Agentic AI workspace powered by LangGraph,
        FastAPI, Streamlit and specialist AI agents
    </div>
    """,
    unsafe_allow_html=True
)