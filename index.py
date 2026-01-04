# For indexing the data -> I need to read this file
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_qdrant import QdrantVectorStore

load_dotenv()


pdf_path = Path(__file__).parent / "HR_policy.pdf"

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path) 
# below will give page by page docs
docs = loader.load() # every page is a doc, so we can iterate on this

# print(docs[12])

# split the docs into smaller chunks
# Overlap will help me understand litle bit a recap of previous chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size= 1000,
    chunk_overlap = 400
)
# This chunks will smaller size of 1000 with overlap of 400, within these two line you converted  your pages into manageable chunks
chunks = text_splitter.split_documents(documents=docs)

# next step to create vector embedding from this chunks   (You can do it manually but LangChain gives you inbuilt utility tool)
# Create Embedding model here
embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-large"
)
# Now the embedding model needs to create chunks and store it vector db
# For that we have bridge

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",         # the place where your database is running
    collection_name = "HR_BOT"
)
print("Indexing of document done")