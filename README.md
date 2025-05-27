# 🧠 Complaint Management Chatbot (RAG + Gemini + FastAPI)

This project is an intelligent chatbot system built using **Streamlit**, **LangChain**, and **Gemini (via Google Generative AI)** to handle:

- 🔍 Document-based question answering using RAG
- 📝 Complaint registration
- 📋 Complaint retrieval using complaint ID

The backend complaint APIs are assumed to be served from a FastAPI server.


---

## 🚀 Features

- **RAG-powered Q&A**: Answers policy-related questions using documents via a retrieval-augmented generation setup.
- **Complaint Registration**: Gathers user details and sends them to the complaint API.
- **Complaint Retrieval**: Retrieves complaint details using a complaint ID.
- **Natural Language Interaction**: Designed to be polite, conversational, and helpful with contextual memory.

---

## 🧪 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt

```

## Create a .env file and include:
```bash
GOOGLE_API_KEY=your_google_gemini_api_key
```



