import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from components.agent_setup import InitializeCustomeAgent
from components.initializer import initialize_components
from components.tools import fetch_tools,format_chat_history


# Streamlit setup
st.set_page_config(page_title="Cyfuture Assesment RAG & Complaint Chatbot", layout="wide")

# initializing agent, tools and retriever
retriever, llm, rag_chain = initialize_components()
rag_tool, complaint_tool, fetch_tool = fetch_tools(llm, rag_chain, st)
agent_init = InitializeCustomeAgent(llm, rag_tool, complaint_tool, fetch_tool)
agent = agent_init.get_agent()


# Streamlit UI
st.title("Cyfuture Assesment Complaint Managment Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display past chat
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_msg)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_msg)

# Chat input
query = st.chat_input("Ask a question or file a complaint...")

if query:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(query)

    formatted_history = format_chat_history(st.session_state.chat_history)

    # Run the agent with manual chat history
    try:
        result = agent.invoke({"input": query, "chat_history": formatted_history})
        response = result["output"]
    except Exception as e:
        response = f"Error: {str(e)}"

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)

    st.session_state.chat_history.append((query, response))

