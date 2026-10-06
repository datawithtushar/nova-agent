import os

import psycopg2
from dotenv import load_dotenv
from langchain.tools import tool


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
# CREATE TASK TABLE
# --------------------------------------------------

def create_task_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            priority TEXT DEFAULT 'Medium',
            due_date TEXT
        )
        """
    )

    connection.commit()

    cursor.close()

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

    """Create a new task in the PostgreSQL database."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            title,
            priority,
            due_date
        )
        VALUES (%s, %s, %s)
        RETURNING task_id
        """,
        (
            title,
            priority,
            due_date
        )
    )

    task_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()

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
        ORDER BY task_id ASC
        """
    )

    tasks = cursor.fetchall()

    cursor.close()

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
                SET {field_name} = %s
                WHERE task_id = %s
                """,
                (
                    new_value,
                    task_id
                )
            )

    connection.commit()

    cursor.close()

    connection.close()

    return "Tasks updated successfully."


# --------------------------------------------------
# INITIALIZE TASK DATABASE
# --------------------------------------------------

create_task_table()