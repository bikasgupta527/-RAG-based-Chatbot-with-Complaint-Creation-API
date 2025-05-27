import os
from langchain_docling import DoclingLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "your-api-key-here")

# Initialize embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Load and process PDF
src_pdf = "data/Policy on Customer Service.pdf"
loader = DoclingLoader(file_path=src_pdf)
docs = loader.load()

# Extract text from documents
texts = [doc.page_content for doc in docs]

# Split texts into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = []
for text in texts:
    split_docs.extend(text_splitter.split_text(text))

# Create FAISS vector store
vectorstore = FAISS.from_texts(split_docs, embedding_model)

# Save FAISS index to disk
index_dir = "faiss_index"
vectorstore.save_local(index_dir)
print(f"FAISS index created and saved to {index_dir}")