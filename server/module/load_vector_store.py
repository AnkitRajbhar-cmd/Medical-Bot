import os
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
# from server.main import vectorstore
from fastapi import Request
load_dotenv()

UPLOAD_DIR = "./uploaded_docs"
CHROMA_DIR = "./chroma_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CHROMA_DIR, exist_ok=True)
#I will made new updations
# Sentence Transformer Embedding Model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
# # sentence-transformers/./
# # Initialize ChromaDB
# vectorstore = Chroma(
#     persist_directory=CHROMA_DIR,
#     embedding_function=embedding_model
# )

# Load, Split, Embed and Store PDF content

def load_vectorstore(uploaded_files,request:Request):
    file_paths = []
    vectorstore = request.app.state.vectorstore
    # Save uploaded PDFs locally
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # Process each PDF
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        print(f"🔍 Processing {len(chunks)} chunks...")

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        print("📤 Storing in ChromaDB...")

        vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )

    # Persist data so it survives restart
    vectorstore.persist()

    print("✅ All documents stored in ChromaDB")
    

def get_retriever():
    """
    Loads already stored Chroma DB and returns retriever
    """
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    return retriever