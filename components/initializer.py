from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from retriever.load_retriever import load_retriever

def initialize_components():
    retriever = load_retriever()
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        max_tokens=None,
        timeout=None,
        max_retries=1,
    )
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
    return retriever, llm, rag_chain

def format_chat_history(chat_history):
    return "\n".join([f"User: {u}\nAssistant: {a}" for u, a in chat_history])

