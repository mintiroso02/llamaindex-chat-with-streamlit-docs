import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
  
st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Citizen's Charter, City Mayor's Office 💬🦙")
st.info("Together we Can Unite", icon="📃")
with st.sidebar:
    st.header("About")
    st.markdown(
        """
       About This Interactive Citizen's Charter

Welcome to the Interactive Citizen's Charter of Gingoog City! 
This program is designed to provide you with quick and accurate 
information about your rights, responsibilities, and the services 
available to you as a resident of Gingoog City.

Features:

Easy Access: Simply input your question or situation, and the program 
will provide you with relevant information based on the 
citizen's charter of Gingoog City.
Comprehensive Information: Our database includes detailed information about various 
services, timelines, and more, as outlined in the official citizen's charter of Gingoog City.
Empowering Citizens: We aim to empower you by giving you access to essential information 
that helps you understand your rights and obligations, and enables you to 
navigate public services effectively.
Disclaimer:

While every effort has been made to ensure the accuracy and relevance of the 
information provided, please note that this program relies on available data 
and may not cover every specific situation. For any legal or official matters, 
we recommend consulting the official documents and authorities of Gingoog City.

Feedback:

Your feedback is valuable to us! If you have any suggestions, encounter any issues, 
or want to contribute to improving this program, please don't hesitate to reach out to us.

Thank you for using the Interactive Citizen's Charter of Gingoog City. 
We hope this tool enhances your experience as a resident and citizen of our community.
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
