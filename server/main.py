from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router
import uvicorn
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

app=FastAPI(title="Medical Assistant API",description="API for AI Medical Assistant Chatbot")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)



# middleware exception handlers
app.middleware("http")(catch_exception_middleware)

CHROMA_DIR = "./chroma_db"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# # Sentence Transformer Embedding Model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
# # sentence-transformers/./
# # Initialize ChromaDB
# vectorstore = Chroma(
#     persist_directory=CHROMA_DIR,
#     embedding_function=embedding_model
# )
# vectorstore = None
app.state.vectorstore = None

@app.on_event("startup")
def startup_event():

    app.state.vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

# routers

# 1. upload pdfs documents
app.include_router(upload_router)
# 2. asking query
app.include_router(ask_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    