from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    "splits the documents into smaller chunks using RecursiveCharacterTextSplitter"

    splitter=RecursiveCharacterTextSplitter( chunk_size=1000, chunk_overlap=200)
    chunks=splitter.split_documents(documents)
    return chunks



