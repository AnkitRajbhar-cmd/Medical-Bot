from fastapi import APIRouter, UploadFile, File,Request
from fastapi.responses import JSONResponse
from module.load_vector_store import load_vectorstore
from typing import List
router=APIRouter()

@router.post("/upload_pdf")
def Upload_Pdf(request : Request,files:List[UploadFile] = File(...)):
    
    abc=load_vectorstore(files,request)
    print("File is used appropriately")
    return JSONResponse(content={"status": "success"})
