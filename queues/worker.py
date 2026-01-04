from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()
openai_client = OpenAI()


# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="HR_BOT",
    embedding=embedding_model,
)


# This process_query is going to run inside a queue worker, we are not going to run directly
def process_query(query:str):
    print("Searching Chunks",query)
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:\n{result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

    SYSTEM_PROMPT = f"""
    You are a helpfull AI assistant who answers user query based on the available context
    retrived from a PDF file along with page_contents and page number.
    You should only answer the user based on the following context and naviagte the user
    to open the right page number to know more

    Context: {context}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":query},
        ]
    )

    print(f">>> {response.choices[0].message.content}")
    return response.choices[0].message.content