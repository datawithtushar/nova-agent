from pathlib import Path

from Rag.document_loader import (
    load_document,
    find_documents,
)

from Rag.vector_store import (
    delete_document_chunks,
    store_chunks,
)

from Rag.text_splitter import split_documents

from Rag.ingestion_tracker import (
    is_file_unchanged,
    mark_file_processed,
    load_history,
)


# --------------------------------------------------
# DOCUMENTS FOLDER
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_FOLDER = BASE_DIR / "Documents"


# --------------------------------------------------
# INGESTION PIPELINE
# --------------------------------------------------

def run_ingestion_pipeline():

    history = load_history()

    files = find_documents(
        DOCUMENTS_FOLDER
    )

    for file in files:

        if is_file_unchanged(
            file,
            history
        ):

            print(
                f"Skipped: {file}"
            )

            continue


        print(
            f"Processing file: {file}"
        )


        documents = load_document(
            file
        )


        chunks = split_documents(
            documents
        )


        delete_document_chunks(
            file
        )


        store_chunks(
            chunks
        )


        mark_file_processed(
            file,
            history
        )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    run_ingestion_pipeline()