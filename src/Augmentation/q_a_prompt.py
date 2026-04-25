from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
def prompt_generation(context,question):
    llm=ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    parser=StrOutputParser()
    prompt=PromptTemplate(
        template="""You are a helpful assistant.
        Answer from the provided pdf,
        If the context is insufficient just say you don't know.
        {context}
        Question:{question}
        """,
        input_variables=['context','question']
        )
    chain= prompt | llm | parser
    

    response=chain.invoke({'context':context,"question":question})
    return response