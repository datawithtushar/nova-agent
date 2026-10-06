import os
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# DATABASE URL
# --------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():

    if not DATABASE_URL:

        raise ValueError(
            "DATABASE_URL is not set."
        )

    return psycopg2.connect(
        DATABASE_URL
    )


# --------------------------------------------------
# CREATE TABLES
# --------------------------------------------------

def create_tables():

    connection = get_connection()

    cursor = connection.cursor()


    # ----------------------------------------------
    # CONVERSATIONS TABLE
    # ----------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            thread_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        """
    )


    # ----------------------------------------------
    # MESSAGES TABLE
    # ----------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            message_id SERIAL PRIMARY KEY,
            thread_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP
        )
        """
    )


    # ----------------------------------------------
    # FEEDBACK TABLE
    # ----------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id SERIAL PRIMARY KEY,
            thread_id TEXT,
            message_id INTEGER,
            feedback TEXT,
            created_at TIMESTAMP
        )
        """
    )


    connection.commit()

    cursor.close()

    connection.close()


# --------------------------------------------------
# CREATE CONVERSATION
# --------------------------------------------------

def create_conversation(
    thread_id: str,
    title: str = "New Chat"
):

    connection = get_connection()

    cursor = connection.cursor()


    now = datetime.now()


    cursor.execute(
        """
        INSERT INTO conversations (
            thread_id,
            title,
            created_at,
            updated_at
        )
        VALUES (%s, %s, %s, %s)

        ON CONFLICT (thread_id)
        DO NOTHING
        """,
        (
            thread_id,
            title,
            now,
            now
        )
    )


    connection.commit()

    cursor.close()

    connection.close()


# --------------------------------------------------
# SAVE MESSAGE
# --------------------------------------------------

def save_message(
    thread_id: str,
    role: str,
    content: str
):

    create_conversation(
        thread_id=thread_id
    )


    connection = get_connection()

    cursor = connection.cursor()


    now = datetime.now()


    # ----------------------------------------------
    # INSERT MESSAGE
    # ----------------------------------------------

    cursor.execute(
        """
        INSERT INTO messages (
            thread_id,
            role,
            content,
            created_at
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            thread_id,
            role,
            content,
            now
        )
    )


    # ----------------------------------------------
    # UPDATE CONVERSATION TIMESTAMP
    # ----------------------------------------------

    cursor.execute(
        """
        UPDATE conversations
        SET updated_at = %s
        WHERE thread_id = %s
        """,
        (
            now,
            thread_id
        )
    )


    connection.commit()

    cursor.close()

    connection.close()


# --------------------------------------------------
# GET MESSAGES
# --------------------------------------------------

def get_messages(
    thread_id: str
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            message_id,
            role,
            content,
            created_at

        FROM messages

        WHERE thread_id = %s

        ORDER BY message_id ASC
        """,
        (
            thread_id,
        )
    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    return rows


# --------------------------------------------------
# GET ALL CONVERSATIONS
# --------------------------------------------------

def get_conversations():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            thread_id,
            title,
            created_at,
            updated_at

        FROM conversations

        ORDER BY updated_at DESC
        """
    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    return rows


# --------------------------------------------------
# SAVE FEEDBACK
# --------------------------------------------------

def save_feedback(
    thread_id: str,
    message_id: int,
    feedback: str
):

    connection = get_connection()

    cursor = connection.cursor()


    now = datetime.now()


    # ----------------------------------------------
    # DELETE PREVIOUS FEEDBACK
    # ----------------------------------------------

    cursor.execute(
        """
        DELETE FROM feedback

        WHERE thread_id = %s
        AND message_id = %s
        """,
        (
            thread_id,
            message_id
        )
    )


    # ----------------------------------------------
    # SAVE NEW FEEDBACK
    # ----------------------------------------------

    cursor.execute(
        """
        INSERT INTO feedback (
            thread_id,
            message_id,
            feedback,
            created_at
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            thread_id,
            message_id,
            feedback,
            now
        )
    )


    connection.commit()

    cursor.close()

    connection.close()


# --------------------------------------------------
# DELETE CONVERSATION
# --------------------------------------------------

def delete_conversation(
    thread_id: str
):

    connection = get_connection()

    cursor = connection.cursor()


    # ----------------------------------------------
    # DELETE FEEDBACK
    # ----------------------------------------------

    cursor.execute(
        """
        DELETE FROM feedback
        WHERE thread_id = %s
        """,
        (
            thread_id,
        )
    )


    # ----------------------------------------------
    # DELETE MESSAGES
    # ----------------------------------------------

    cursor.execute(
        """
        DELETE FROM messages
        WHERE thread_id = %s
        """,
        (
            thread_id,
        )
    )


    # ----------------------------------------------
    # DELETE CONVERSATION
    # ----------------------------------------------

    cursor.execute(
        """
        DELETE FROM conversations
        WHERE thread_id = %s
        """,
        (
            thread_id,
        )
    )


    connection.commit()

    cursor.close()

    connection.close()


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_tables()