from fastapi import FastAPI,APIRouter
from src.ingestions.retrievers import get_retrievers
from pydantic import BaseModel
from src.Augmentation.q_a_prompt import prompt_generation

router=APIRouter()

class ChatRequestt(BaseModel):
    question:str

@router.post("/chat")

async def chat(request: ChatRequestt):
    retrieved_docs=get_retrievers(request.question)
    context= "\n\n".join(doc.page_content for doc in retrieved_docs)

    answer=prompt_generation(context,request.question)

    return {"answer":answer}