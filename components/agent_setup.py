from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate


class InitializeCustomeAgent:
    def __init__(self,llm, rag_tool, complaint_tool, fetch_tool):
        self.llm = llm
        self.rag_tool = rag_tool
        self.complaint_tool = complaint_tool
        self.fetch_tool = fetch_tool

    def get_agent(self):
        prompt = PromptTemplate(
            input_variables=["input", "chat_history"],
            template=(
                "You are a helpful AI assistant chatbot that can answer queries related to policy of the customers and also manage complaints.\n"
                "Your answer will be restricted to give the answers related policies of customers and filing and retrieving complaints"
                "If the user wants to do a chitchat do a proper chit with humor"
                "Based on the user complaint identify the issue by yourself, don't ask for the detailed description.\n"
                "format the output of tools in natural language"
                "convert the tool messages in natural language"
                "convert your observations in conversational language"
                "Output format should in natural languages if you are asking for missing field ask nicely that please provide me with some of your information like name, phone number, email id and complaint details"
                "Once you get all the information (name, email, phone, and complaint description), call ComplaintRegistrationTool.\n"
                "You have access to the following tools:\n"
                "1. RAGQueryTool - use for general document-based questions.\n"
                "2. ComplaintRegistrationTool - ONLY use when all of: name, phone_no, email_id, complaint_detail.\n"
                "3. FetchComplaintInformationTool - use when a complaint_id is provided to fetch details.\n\n"
                "Chat history:\n{chat_history}\n\n"
                "User input: {input}\n"
            )
        )

        # Initialize Agent (no memory)
        agent = initialize_agent(
            tools=[self.rag_tool, self.complaint_tool, self.fetch_tool],
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={"prompt": prompt}
        )
        return agent