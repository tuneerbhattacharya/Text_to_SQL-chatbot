from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def build_vector_db(schema_chunks, openai_key: str):
    return FAISS.from_texts(schema_chunks, OpenAIEmbeddings(api_key=openai_key))


def retrieve_context(vector_db, query: str, k: int = 4):
    docs = vector_db.similarity_search(query, k=k)
    return "\n\n".join(d.page_content for d in docs)
