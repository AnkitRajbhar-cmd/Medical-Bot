
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from module.get_llm_chain import get_llm_chain
from module.query_handler import query_chain
from logger import logger
from module.load_vector_store import get_retriever

router = APIRouter()

  # load once (efficient)

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        retriever=get_retriever()
        
        chain = get_llm_chain(retriever) 
        
        result = query_chain(chain, question)

        logger.info("query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})
