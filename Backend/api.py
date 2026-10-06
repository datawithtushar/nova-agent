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
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Agentic AI Assistant API",
    version="1.0"
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
        "status": "ok"
    }


# --------------------------------------------------
# CHAT
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        result = run_chat(
            question=request.question,
            thread_id=request.thread_id
        )

        return {
            "answer": result.get(
                "answer",
                "No answer was generated."
            ),

            "execution_mode": result.get(
                "execution_mode",
                "single"
            ),

            "selected_agents": result.get(
                "selected_agents",
                []
            ),

            "sources": result.get(
                "sources",
                []
            ),
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
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

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
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

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
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


        return {
            "status": "success",
            "message": "Feedback saved."
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
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


        return {
            "status": "success",
            "message": "Conversation deleted."
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )