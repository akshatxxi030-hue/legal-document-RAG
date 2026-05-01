from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import redis
import os
import hashlib
import json


load_dotenv()
REDIS_URL=os.getenv("REDIS_URL")
r=redis.from_url(REDIS_URL)


def red_flags(docs):

    full_text=" ".join([doc.page_content for doc in docs])
    full_text=full_text[:15000]
    cache_key="red_flag:"+hashlib.md5(full_text.encode()).hexdigest()
    cached=r.get(cache_key)
    if cached:
        print("cache hit")
        return json.loads(cached)

    llm=ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    parser=StrOutputParser()

    prompt=PromptTemplate(
        template="""""
        You are a legal analyst .
        Extract all the red flags that exist in the document.
        Document:{document}
        List out the red flags
        Do not use markdowns or asterisks.
        Use a proper human eye pleasing formatting""",
        input_variables=['document']
    )

    chain=prompt | llm | parser

    response=chain.invoke({"document":full_text})

    r.setex(cache_key,3600,json.dumps(response))
    
    return response