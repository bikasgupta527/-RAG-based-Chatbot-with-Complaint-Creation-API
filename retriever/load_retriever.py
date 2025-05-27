import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

def load_retriever():
    """Loads the saved FAISS index and returns the retriever."""
    # Load environment variables
    load_dotenv()
 
    # Initialize embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # Load FAISS index
    index_dir = "faiss_index"
    if not os.path.exists(index_dir):
        raise FileNotFoundError(
            f"FAISS index not found at {index_dir}. Please run create_faiss_index.py first."
        )
    
    vectorstore = FAISS.load_local(
        index_dir,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore.as_retriever()