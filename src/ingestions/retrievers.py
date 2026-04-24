from vector_store import store_embeddings,get_pinecone_index    
from embeddings import get_embeddings
from langchain_pinecone import PineconeVectorStore
import os

def get_retrievers():
    embeddings=get_embeddings()
    vectorstore=PineconeVectorStore.from_existing_index(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embeddings=embeddings
    )

    return vectorstore.as_retriever(search_kwargs={"k":5})
