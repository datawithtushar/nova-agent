import os
import sqlite3
from pathlib import Path

from langchain.tools import tool


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
    / "tasks.db"
)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )


# --------------------------------------------------
# CREATE TASK TABLE
# --------------------------------------------------

def create_task_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            priority TEXT DEFAULT 'Medium',
            due_date TEXT
        )
        """
    )

    connection.commit()

    connection.close()

    return "Task table created successfully."


# --------------------------------------------------
# 1) CREATE TASK
# --------------------------------------------------

@tool
def create_task(
    title,
    priority="Medium",
    due_date=None
):

    """Create a new task in the SQLite database."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            title,
            priority,
            due_date
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            priority,
            due_date
        )
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return (
        f"Task {task_id} created successfully."
    )


# --------------------------------------------------
# 2) GET TASKS
# --------------------------------------------------

@tool
def get_tasks():

    """Get all tasks."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            task_id,
            title,
            status,
            priority,
            due_date

        FROM tasks
        """
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


# --------------------------------------------------
# 3) UPDATE TASKS
# --------------------------------------------------

@tool
def update_tasks(
    updates: dict
):

    """Update one or more tasks."""

    connection = get_connection()

    cursor = connection.cursor()


    allowed_fields = [
        "title",
        "status",
        "priority",
        "due_date"
    ]


    for task_id, fields in updates.items():

        for field_name, new_value in fields.items():

            if field_name not in allowed_fields:
                continue

            cursor.execute(
                f"""
                UPDATE tasks
                SET {field_name} = ?
                WHERE task_id = ?
                """,
                (
                    new_value,
                    task_id
                )
            )


    connection.commit()

    connection.close()

    return "Tasks updated successfully."


# --------------------------------------------------
# INITIALIZE TASK DATABASE
# --------------------------------------------------

create_task_table()