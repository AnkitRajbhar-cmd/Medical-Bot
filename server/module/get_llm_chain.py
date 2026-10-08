from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from module.load_vector_store import load_vectorstore
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_chain(retriever):

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant"
    )

    # vectordb = load_vectorstore()
    # retriever = vectordb.as_retriever(search_kwargs={"k":3})

    prompt = ChatPromptTemplate.from_template("""
You are MediBot, an AI assistant helping users understand medical documents.

Context:
{context}

Question:
{question}

Rules:
- Be calm and factual
- Use simple language
- If answer not found, say:
"I'm sorry, but I couldn't find relevant information in the provided documents."
- Do NOT give medical advice

Answer:
""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain= (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
  