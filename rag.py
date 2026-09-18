import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# ... (Keep your existing embeddings, DB_PATH, and DOCS_PATH variables)

def initialize_vector_store():
    """Reads local TXT and PDF files, splits them, and stores them in ChromaDB."""
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)
        print(f"[!] Created {DOCS_PATH}. Please drop your PDFs and text files here.")

    documents = []

    # 1. Load all text files
    txt_loader = DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents.extend(txt_loader.load())

    # 2. Load all PDF files
    pdf_loader = DirectoryLoader(DOCS_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents.extend(pdf_loader.load())

    if not documents:
        print("[!] No documents found to index.")
        return None

    # Split documents into manageable chunks because embedding models have limited context windows
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(documents)

    # Persist embeddings into local Chroma vector store
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"[+] Successfully indexed {len(splits)} chunks into ChromaDB.")
    return vector_store