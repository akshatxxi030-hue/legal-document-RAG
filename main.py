from fastapi import FastAPI
from src.api.routes import upload,chat,summarize,risks

app=FastAPI(title="Legal AI API")

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(summarize.router)
app.include_router(risks.router)