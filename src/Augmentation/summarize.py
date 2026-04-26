from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def summary(docs):

    full_text=" ".join([doc.page_content for doc in docs])
    full_text=full_text[:15000]
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
        Provide a structured summary""",
        

        input_variables=['document']
    )

    chain=Prompt | llm | parser

    response=chain.invoke({"document":full_text})
    return response