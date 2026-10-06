import hashlib
import json
from pathlib import Path


HISTORY_FILE = Path("data/ingestion_history.json")


def create_file_hash(file_path):
    """Create a unique hash from the file contents. """

    hasher = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(8192)

            if not data:
                break

            hasher.update(data)

    return hasher.hexdigest()


def load_history():
    """Load previously processed file hashes."""

    if not HISTORY_FILE.exists():
        return {}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    """Save processed file hashes."""

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=2,
        )


def is_file_unchanged(file_path, history):
    """Check whether the file has already been processedand has not changed."""

    file_path = Path(file_path)

    current_hash = create_file_hash(file_path)
    stored_hash = history.get(str(file_path))

    return current_hash == stored_hash


def mark_file_processed(file_path, history):
    """ Store the current file hash after successful processing. """

    file_path = Path(file_path)

    history[str(file_path)] = create_file_hash(file_path)

    save_history(history)