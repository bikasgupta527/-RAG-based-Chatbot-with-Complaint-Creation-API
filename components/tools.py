from langchain.tools import Tool
import requests

# Format chat history for prompt
def format_chat_history(chat_history):
    return "\n".join([f"User: {u}\nAssistant: {a}" for u, a in chat_history])

def fetch_tools(llm, rag_chain, st):
    # Tool: RAG QA
    def rag_query_fn(query: str) -> str:
        result = rag_chain.invoke(query)
        return result["result"]

    rag_tool = Tool(
        name="RAGQueryTool",
        func=rag_query_fn,
        description="Use this tool to answer general questions based on documents and knowledge base. Input should be the user query. format the output in natural language so user can understand and it be conversational",
        return_direct=True
    )

    # Tool: Complaint Registration
    def register_complaint_str(input_str: str) -> str:
        try:
            parts = {
                kv.split("=")[0].strip(): kv.split("=")[1].strip()
                for kv in input_str.split(",")
            }
            required_fields = ["name", "phone_no", "email_id", "complaint_detail"]
            missing_fields = [field for field in required_fields if field not in parts or not parts[field]]

            if missing_fields:
                # Use LLM to generate a polite message
                missing_fields_str = ", ".join(missing_fields)
                formatted_history = format_chat_history(st.session_state.chat_history)
                prompt = f"""The user tried to register a complaint but forgot to provide the following: {missing_fields_str}. Generate a friendly and professional response asking the user to provide those fields. the response should be short. ask the user please please provide the details like
                I am passing the chat history for your reference. Based on this generate your response \n
                {formatted_history}
                """


                polite_response = llm.invoke(prompt).content
                return polite_response
            name = parts["name"]
            phone_no = parts["phone_no"]
            email_id = parts["email_id"]
            complaint_detail = parts["complaint_detail"]
        except Exception as e:
            return f"Invalid input. Use: name=..., phone_no=..., email_id=..., complaint_detail=... | Error: {str(e)}"

        try:
            api_url = "http://127.0.0.1:8000/complaints"
            payload = {
                "name": name,
                "phone_number": phone_no,
                "email": email_id,
                "complaint_details": complaint_detail
            }
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            return (
                f"complaint has been registered with ID: "
                f"{response_data['complaint_id']}"
            )
        except Exception as e:
            return f"Error registering complaint: {str(e)}"

    complaint_tool = Tool(
        name="ComplaintRegistrationTool",
        func=register_complaint_str,
        description=(
            "Use this tool ONLY when you have all of the following: name, phone_no, email_id, and complaint_detail. "
            "Ask the user to provide any missing information if needed.\n"
            "return the answer in natural conversational language"
            "based on the returned response of the tool convert the variables names in natural language not in coding language"
            "Identifies complaint based on user input and never asks complaint in details.\n"
            "Input format: name=..., phone_no=..., email_id=..., complaint_detail=..."
            "Output format should in natural languages if you are asking for missing field ask nicely that please provide me with some of your information like name, phone number, email id and complaint details"
        ),
        return_direct=True
    )

    # Tool: Complaint Fetch
    def fetch_complaint(complaint_id: str) -> str:
        try:
            api_url = "http://127.0.0.1:8000/complaints/search"
            params = {"complaint_id": complaint_id}
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            response_data = response.json()[0]
            return (
                f"Complaint ID: {response_data.get('complaint_id', 'N/A')}\n"
                f"Name: {response_data.get('name', 'N/A')}\n"
                f"Phone: {response_data.get('phone_number', 'N/A')}\n"
                f"Email: {response_data.get('email', 'N/A')}\n"
                f"Details: {response_data.get('complaint_details', 'N/A')}"
            )
        except Exception as e:
            return f"Error fetching complaint: {str(e)}"

    fetch_tool = Tool(
        name="FetchComplaintInformationTool",
        func=fetch_complaint,
        description="Use this tool to fetch a complaint's details. Input should be the complaint_id only.",
        return_direct=True
    )

    return rag_tool, complaint_tool, fetch_tool
