from fastapi import FastAPI, APIRouter
from src.ingestions.text_splitter import split_documents
from src.ingestions.loaders import pdf_loader 