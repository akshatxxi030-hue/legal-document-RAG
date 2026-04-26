from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def red_flags(docs):

    full_text=" ".join([doc.page_content for doc in docs])
    full_text=full_text[:15000]
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
    return response