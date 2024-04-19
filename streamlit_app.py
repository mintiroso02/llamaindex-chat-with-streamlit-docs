import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
st.set_page_config(page_title="Gingoog City Citizen Charter, page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Citizen's Charter, City Mayor's Office 💬🦙")
st.info("Together we Can Unite", icon="📃")
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Welcome to the AI-Integrated Citizen's Charter System, 
        designed to streamline and enhance the efficiency of 
        public service delivery. Our system leverages the power 
        of artificial intelligence (AI) to provide a seamless and 
        transparent experience for citizens availing services 
        from government offices.

        Key Features:

        Efficient Service Processing: The system automates 
        various processes involved in service delivery, reducing 
        processing times and enhancing overall efficiency.

        Transparent and Accessible: Citizens can easily access 
        information about the services offered, requirements, 
        processing steps, and fees through an intuitive online platform.

        AI-Powered Assistance: Our AI technology provides personalized 
        assistance to citizens, guiding them through the steps required 
        to avail services and answering common queries in real-time.

        Integrated Database: The system maintains a centralized database 
        of services, requirements, client information, payments, and issued 
        clearances, ensuring data accuracy and consistency.

        Citizen Feedback Mechanism: We value citizen feedback and have 
        incorporated a feedback mechanism to gather input on service quality, 
        allowing us to continuously improve our services.

        Benefits for Citizens:

        Simplified Process: Citizens can easily navigate through the service 
        requirements and steps, reducing confusion and improving user experience.
        
        Time and Cost Savings: The streamlined process and reduced processing 
        times save citizens valuable time and effort.
        
        Transparency: Citizens have access to transparent information about service 
        fees, processing times, and requirements, promoting accountability and trust.
        
        Improved Service Quality: AI integration enables quick resolution of queries 
        and issues, leading to better service delivery and customer satisfaction.
        
        How to Use the System:

        Visit our online platform or mobile app to access the list of services 
        offered by government offices.
        
        Select the desired service and review the checklist of requirements, 
        processing steps, and fees.
        
        Follow the guided steps provided by the AI assistant to submit necessary 
        documents and complete the payment process.
        
        
        Provide feedback on your experience to help us enhance our services further.
        At AI-Integrated Citizen's Charter System, we are committed to leveraging technology to create a more citizen-centric and efficient public service environment. We strive to provide accessible, transparent, and high-quality services that meet the needs of our citizens effectively.
        """
    )
    st.header("Example Questions")

    st.markdown("- What are the requirements to obtain a Barangay Clearance?")
    st.markdown("- How can I secure a Police Clearance?")
    st.markdown("- What are the steps for applying for a Vacation Leave or Sick Leave?")
    st.markdown("- Where can I get a Certification for IP group membership or lineage?")
    st.markdown("- What is the processing time for issuing a Mayor's Clearance?")
    st.markdown("- Who oversees the processing of a Scholarship Contract Issuance?")
    st.markdown("- Which services are available at the City Treasurer’s Office (CTO)?")
    st.markdown("- Who is in charge of managing the Leave of Absence service?")
    st.markdown("- What are the fees for a Solo Parent Leave (maximum of 7 Days)?")
    st.markdown("- What is the average processing time for obtaining a Barangay Clearance?")
    st.markdown("- Which services have the longest processing time?")
    st.markdown(
        "- Provide a list of all requirements for applying for a Special Privileged Leave (SPL) (maximum of 3 Days).")
    st.markdown("- What is the current wait time for processing Biodata and latest grades?")
    st.markdown("- Who is responsible for reviewing and signing the Scholarship Contract?")
  
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the Citizen's Charter"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert o$
        # index = VectorStoreIndex.from_documents(docs)
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are a helpful assistant tasked with assisting citizens regarding the Citizen's Charter of Gingoog City. You provide accurate information about the services. Your responses should be clear and informative, ensuring that users understand the procedures, requirements, and benefits of each service. Assume that all questions are related to the Citizen's Charter. Keep your answers as detailed as possible and based on facts – do not hallucinate information. Also, note that citizens may use different languages, so you need to respond according to their preferences. Be mindful also if they ask situational questions; you should answer them."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
