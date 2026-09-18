import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

DOCS_PATH = "./docs"
DB_PATH = "./chroma_db"

def build_index():
    print("[*] Scanning ./docs for PDFs and TXT files...")
    documents = []

    # Load TXT and PDF files
    if os.path.exists(DOCS_PATH):
        documents.extend(DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader).load())
        documents.extend(DirectoryLoader(DOCS_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader).load())
    
    if not documents:
        print("[!] No files found. Drop some PDFs/text notes in ./docs and run again.")
        return

    # Split and Embed
    print("[*] Chunking documents and generating vectors via Ollama...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Save to ChromaDB
    Chroma.from_documents(splits, embeddings, persist_directory=DB_PATH)
    print(f"[+] Success! {len(splits)} chunks indexed into {DB_PATH}. EV is ready to read.")

if __name__ == "__main__":
    build_index()