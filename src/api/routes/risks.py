from fastapi import FastAPI,APIRouter,HTTPException,File,UploadFile
from pydantic import BaseModel
from src.Augmentation.red_flags import red_flags,r
from src.ingestions.loaders import pdf_loader
from src.api.routes.upload import  upload_document
import os
import json
import hashlib



router=APIRouter()

class RedFlagRequest(BaseModel):
    filename:str

@router.post("/redflag")
async def summary_gen(request:RedFlagRequest):
    temp_path=f"temp/{request.filename}"
    
    if not os.path.exists(temp_path):
        raise HTTPException(status_code=404,detail="File not found. Please upload it first")
    cache_key = "red_flag:" + hashlib.md5(request.filename.encode()).hexdigest()
    try:
        cached=r.get(cache_key)
        if cached:
            print("FAST Cache Hit! Bypassing PDF loader.")
            return{
                "filename":request.filename,
                "red flags":json.loads(cached)
            }
    except Exception as e:
        print(f"Redis Cache GET Error in route: {e}")

         
    docs=pdf_loader(temp_path)
    red_flag=red_flags(docs,filename=request.filename)



    return{"filename":request.filename,"red flags":red_flag}
    