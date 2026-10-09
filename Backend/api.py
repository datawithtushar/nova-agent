import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Backend.chat_service import run_chat

from Database.conversation_db import (
    get_conversations,
    get_messages,
    save_feedback,
    delete_conversation,
)


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("nova-backend")


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Nova API",
    description="Backend API for the Nova multi-agent AI assistant.",
    version="1.0.0"
)


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    thread_id: str


class FeedbackRequest(BaseModel):
    thread_id: str
    message_id: int
    feedback: str


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "nova-backend",
        "version": "1.0.0"
    }


# --------------------------------------------------
# CHAT
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        logger.info(
            "Chat request received | thread_id=%s",
            request.thread_id
        )

        result = run_chat(
            question=request.question,
            thread_id=request.thread_id
        )

        execution_mode = result.get(
            "execution_mode",
            "single"
        )

        selected_agents = result.get(
            "selected_agents",
            []
        )

        logger.info(
            "Chat completed | thread_id=%s | mode=%s | agents=%s",
            request.thread_id,
            execution_mode,
            selected_agents
        )

        return {
            "answer": result.get(
                "answer",
                "No answer was generated."
            ),

            "execution_mode": execution_mode,

            "selected_agents": selected_agents,

            "sources": result.get(
                "sources",
                []
            ),
        }


    except Exception:

        logger.exception(
            "Chat processing failed | thread_id=%s",
            request.thread_id
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Nova was unable to process this request. "
                "Please try again."
            )
        )


# --------------------------------------------------
# GET ALL CONVERSATIONS
# --------------------------------------------------

@app.get("/conversations")
def conversations():

    try:

        rows = get_conversations()

        return [
            {
                "thread_id": thread_id,
                "title": title,
                "created_at": created_at,
                "updated_at": updated_at,
            }
            for (
                thread_id,
                title,
                created_at,
                updated_at
            ) in rows
        ]


    except Exception:

        logger.exception(
            "Unable to retrieve conversations."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load conversations "
                "at the moment."
            )
        )


# --------------------------------------------------
# GET CONVERSATION MESSAGES
# --------------------------------------------------

@app.get("/conversations/{thread_id}")
def conversation(thread_id: str):

    try:

        rows = get_messages(
            thread_id
        )

        return [
            {
                "message_id": message_id,
                "role": role,
                "content": content,
                "created_at": created_at,
            }
            for (
                message_id,
                role,
                content,
                created_at
            ) in rows
        ]


    except Exception:

        logger.exception(
            "Unable to retrieve conversation | thread_id=%s",
            thread_id
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load this conversation "
                "at the moment."
            )
        )


# --------------------------------------------------
# SAVE FEEDBACK
# --------------------------------------------------

@app.post("/feedback")
def feedback(request: FeedbackRequest):

    try:

        valid_feedback = [
            "positive",
            "negative"
        ]

        if request.feedback not in valid_feedback:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Feedback must be either "
                    "'positive' or 'negative'."
                )
            )


        save_feedback(
            thread_id=request.thread_id,
            message_id=request.message_id,
            feedback=request.feedback
        )


        logger.info(
            "Feedback saved | thread_id=%s | message_id=%s",
            request.thread_id,
            request.message_id
        )


        return {
            "status": "success",
            "message": "Feedback saved."
        }


    except HTTPException:

        raise


    except Exception:

        logger.exception(
            "Unable to save feedback | thread_id=%s | message_id=%s",
            request.thread_id,
            request.message_id
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to save feedback "
                "at the moment."
            )
        )


# --------------------------------------------------
# DELETE CONVERSATION
# --------------------------------------------------

@app.delete("/conversations/{thread_id}")
def remove_conversation(thread_id: str):

    try:

        delete_conversation(
            thread_id
        )


        logger.info(
            "Conversation deleted | thread_id=%s",
            thread_id
        )


        return {
            "status": "success",
            "message": "Conversation deleted."
        }


    except Exception:

        logger.exception(
            "Unable to delete conversation | thread_id=%s",
            thread_id
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to delete the conversation "
                "at the moment."
            )
        )