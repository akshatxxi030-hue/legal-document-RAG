from fastapi import FastAPI,APIRouter,HTTPException,File,UploadFile
from pydantic import BaseModel
from src.Augmentation.summarize import summary
from src.ingestions.loaders import pdf_loader
from src.api.routes.upload import  upload_document
import os

router=APIRouter()

class SummaryRequest(BaseModel):
    filename:str

@router.post("/summary")
async def summary_gen(request:SummaryRequest):
    temp_path=f"temp/{request.filename}"
    
    if not os.path.exists(temp_path):
        raise HTTPException(status_code=404,detail="File not found. Please upload it first")
    
    docs=pdf_loader(temp_path)

    result_summary=summary(docs)

    return{
        "filename":request.filename,"result_summary":result_summary
    }
    

    

