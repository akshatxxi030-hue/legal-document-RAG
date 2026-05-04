from fastapi import FastAPI,APIRouter,HTTPException,File,UploadFile
from pydantic import BaseModel
from src.Augmentation.summarize import summary, r
from src.ingestions.loaders import pdf_loader
from src.api.routes.upload import  upload_document
import os
import json
import hashlib


router=APIRouter()

class SummaryRequest(BaseModel):
    filename:str

@router.post("/summary")
async def summary_gen(request:SummaryRequest):
    temp_path=f"temp/{request.filename}"
    
    if not os.path.exists(temp_path):
        raise HTTPException(status_code=404,detail="File not found. Please upload it first")
    
    # 1. Fast Cache Check (Before loading PDF)
    cache_key = "summary_file:" + hashlib.md5(request.filename.encode()).hexdigest()
    try:
        cached = r.get(cache_key)
        if cached:
            print("FAST Cache Hit! Bypassing PDF loader.")
            return {
                "filename": request.filename,
                "result_summary": json.loads(cached)
            }
    except Exception as e:
        print(f"Redis Cache GET Error in route: {e}")

    # 2. If no cache, load the heavy PDF
    docs=pdf_loader(temp_path)

    # 3. Generate summary and pass filename so it can save to cache
    result_summary=summary(docs, filename=request.filename)

    
    return{
        "filename":request.filename,"result_summary":result_summary
    }
    

    

