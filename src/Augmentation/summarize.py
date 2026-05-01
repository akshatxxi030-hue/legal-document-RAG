from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import hashlib
import redis
import os
import json



load_dotenv()
REDIS_URL=os.getenv("REDIS_URL")
r=redis.from_url(REDIS_URL)

def summary(docs):

    full_text=" ".join([doc.page_content for doc in docs])
    full_text=full_text[:15000]

    cache_key="summary:"+hashlib.md5(full_text.encode()).hexdigest()
    cached=r.get(cache_key)
    if cached:
        print("cache hit")
        return json.loads(cached)   
    llm=ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    parser=StrOutputParser()

    Prompt=PromptTemplate(
        template="""""You are a legal analyst.
        Summarize this legal document clearly :
        - Main purpose of the document
        - Important dates and deadlines
        - Key parties involved
        - Critical obligations
        - Key terms and conditions
        
        Document:{document}
        Provide a structured summary
        Do not use markdowns or asterisks.
        Use a proper human eye pleasing formatting""",
        

        input_variables=['document']
    )

    chain=Prompt | llm | parser

    response=chain.invoke({"document":full_text})

    r.setex(cache_key,3600,json.dumps(response))
    
    return response