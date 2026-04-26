from fastapi import FastAPI, APIRouter,UploadFile,File
from src.ingestions.text_splitter import split_documents
from src.ingestions.loaders import pdf_loader 
from src.ingestions.embeddings import get_embeddings
from src.ingestions.vector_store import store_embeddings
import os
import shutil

router=APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    temp_path=f"temp/{file.filename}"
    os.makedirs("temp",exist_ok=True)
    with open(temp_path,"wb") as f:
        shutil.copyfileobj(file.file,f)

    docs=pdf_loader(temp_path)
    chunks=split_documents(docs)
    embeddings=get_embeddings()
    store_embeddings(chunks)

    return {"message":"Document Uploaded Successfully","filename":file.filename}
