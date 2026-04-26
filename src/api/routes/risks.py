from fastapi import FastAPI,APIRouter,HTTPException,File,UploadFile
from pydantic import BaseModel
from src.Augmentation.red_flags import red_flags
from src.ingestions.loaders import pdf_loader
from src.api.routes.upload import  upload_document
import os

router=APIRouter()

class RedFlagRequest(BaseModel):
    filename:str

@router.post("/redflag")
async def summary_gen(request:RedFlagRequest):
    temp_path=f"temp/{request.filename}"
    
    if not os.path.exists(temp_path):
        raise HTTPException(status_code=404,detail="File not found. Please upload it first")
    
    docs=pdf_loader(temp_path)
    
    red_flag=red_flags(docs)

    return{"filename":request.filename,"red flags":red_flag}
    