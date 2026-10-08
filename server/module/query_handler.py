from logger import logger



def query_chain(chain, user_input:str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result = chain.invoke(user_input)
        return {"answer": result}
    except Exception as e:
        logger.exception("Chain failed")
        return {"error": str(e)}