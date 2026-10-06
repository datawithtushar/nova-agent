from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader

# Loading & checking PDF files----------------------------------------------------------------------------------------

SUPPORTED_FILE_TYPES = {".pdf", ".docx"}


def find_documents(folder_path: str):
    """Find all supported documents inside the folder and subfolders."""

    documents_folder = Path(folder_path)

    if not documents_folder.exists():
        raise FileNotFoundError(
            f"Documents folder not found: {documents_folder}"
        )

    files = [
        file_path
        for file_path in documents_folder.rglob("*")
        if (
            file_path.is_file()
            and file_path.suffix.lower() in SUPPORTED_FILE_TYPES
        )
    ]

    return files


def load_document(file_path):
    """Load one PDF or DOCX document."""

    file_path = Path(file_path)
    file_type = file_path.suffix.lower()

    if file_type == ".pdf":
        loader = PyPDFLoader(str(file_path))

    elif file_type == ".docx":
        loader = Docx2txtLoader(str(file_path))

    else:
        raise ValueError(
            f"Unsupported file type: {file_type}"
        )

    documents = loader.load()

    for document in documents:
        document.metadata["file_name"] = file_path.name
        document.metadata["file_type"] = file_type
        document.metadata["source"] = str(file_path)

    return documents