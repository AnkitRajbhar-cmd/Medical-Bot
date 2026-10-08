import asyncio
from fastapi import FastAPI
from module.get_llm_chain import get_llm_chain
# from langchain_core.output_parsers import pydanticparser

app=FastAPI()

@app.get("/welcome")
def Welcome(query:str):
    res=get_llm_chain(query)
    
    return {"result":res}
    
    # return{"response":"Welcome new user"}//
    
# if __name__=="__main__":
#     asyncio.run()