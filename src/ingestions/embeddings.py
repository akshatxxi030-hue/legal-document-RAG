from langchain_openai import OpenAIEmbeddings

def get_embeddings():
    embeddings=OpenAIEmbeddings(
        model_name="text-embedding-3-small"
    )
    return embeddings