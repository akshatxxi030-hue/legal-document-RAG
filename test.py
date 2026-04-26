from src.ingestions.loaders import pdf_loader
from src.ingestions.text_splitter import split_documents
from src.ingestions.embeddings import get_embeddings
from src.ingestions.vector_store import store_embeddings,get_pinecone_index
from src.ingestions.retrievers import  get_retrievers
from src.Augmentation.q_a_prompt import prompt_generation
from src.Augmentation.summarize import summary
from src.Augmentation.red_flags import red_flags

#loader
docs=pdf_loader("D:\THIS PC\python_workspace\legal_ai_rag\pages-29-deed-sample.pdf")
print(f"loaded {len(docs)}pages")

#text splitting
#print('splitting')
#chunks=split_documents(docs)
#print(f"split into {len(chunks)}chunks")

#embedding generation
#print("generating embeddings")
#embedding=get_embeddings()
#print(f"embeddings created")

#Pinecone index
#get_pinecone_index()

#storing in pinecone 
#print("storing in pinecone")
#store_embeddings(chunks)
#print("stored in pinecone")

#retrieving
#print("Retriving relevant chunks")
#question="What is this document about"
#retrieved_docs=get_retrievers(question)
#context="\n\n".join(doc.page_content for doc in retrieved_docs)
#print(f"Retrieved {len(retrieved_docs)}chunks")

#generation
#print("Generating answer")
#answer=prompt_generation(context,question)
#print(f"Answer{answer}")

#Test summary

#print("Generating summary")
#summarise=summary(docs)
#print(f"Summary: {summarise}")

red=red_flags(docs)
print(f"redf flag:{red}")