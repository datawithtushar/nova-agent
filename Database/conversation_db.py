import os
import sqlite3
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# DATABASE DIRECTORY
# --------------------------------------------------

DEFAULT_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
)

DATA_DIR = Path(
    os.getenv(
        "DATA_DIR",
        str(DEFAULT_DATA_DIR)
    )
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------

DB_PATH = (
    DATA_DIR
    / "conversations.db"
)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():

    connection = sqlite3.connect(
        DB_PATH
    )

    return connection


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
            created_at TEXT,
            updated_at TEXT
        )
        """
    )


    # ----------------------------------------------
    # MESSAGES TABLE
    # ----------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
        """
    )


    # ----------------------------------------------
    # FEEDBACK TABLE
    # ----------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            message_id INTEGER,
            feedback TEXT,
            created_at TEXT
        )
        """
    )


    connection.commit()

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


    now = datetime.now().isoformat()


    cursor.execute(
        """
        INSERT OR IGNORE INTO conversations (
            thread_id,
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            thread_id,
            title,
            now,
            now
        )
    )


    connection.commit()

    connection.close()


# --------------------------------------------------
# SAVE MESSAGE
# --------------------------------------------------

def save_message(
    thread_id: str,
    role: str,
    content: str
):

    # Ensure conversation exists
    create_conversation(
        thread_id=thread_id
    )


    connection = get_connection()

    cursor = connection.cursor()


    now = datetime.now().isoformat()


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
        VALUES (?, ?, ?, ?)
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
        SET updated_at = ?
        WHERE thread_id = ?
        """,
        (
            now,
            thread_id
        )
    )


    connection.commit()

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

        WHERE thread_id = ?

        ORDER BY message_id ASC
        """,
        (
            thread_id,
        )
    )


    rows = cursor.fetchall()


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


    now = datetime.now().isoformat()


    # ----------------------------------------------
    # REMOVE PREVIOUS FEEDBACK
    # ----------------------------------------------
    #
    # Only one feedback value is stored for each
    # assistant response.
    # ----------------------------------------------

    cursor.execute(
        """
        DELETE FROM feedback

        WHERE thread_id = ?
        AND message_id = ?
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
        VALUES (?, ?, ?, ?)
        """,
        (
            thread_id,
            message_id,
            feedback,
            now
        )
    )


    connection.commit()

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
        WHERE thread_id = ?
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
        WHERE thread_id = ?
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
        WHERE thread_id = ?
        """,
        (
            thread_id,
        )
    )


    connection.commit()

    connection.close()


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_tables()