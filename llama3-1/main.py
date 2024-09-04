import json
import os
import streamlit as st
from langchain_community.llms import Ollama  
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

JSON_FILE_PATH = r'C:\Users\monia.fawzi\Downloads\ai json\llama3-1\sample2.json'

def process_json_file(json_data):
    def flatten_json(y):
        """Helper function to flatten nested JSON."""
        def flatten(x, name=''):
            if isinstance(x, dict):
                for a in x:
                    flatten(x[a], name + a + '_')
            elif isinstance(x, list):
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        out = {}
        flatten(y)
        return out

    flattened_data = flatten_json(json_data)
    combined_text = " ".join([f"{k}: {v}" for k, v in flattened_data.items()])
    return combined_text

# Load and process the JSON file at startup
@st.cache_resource
def load_and_process_json():
    if not os.path.isfile(JSON_FILE_PATH):
        st.write("JSON file not found.")
        return None

    with open(JSON_FILE_PATH, 'r') as file:
        json_data = json.load(file)
    
    processed_text = process_json_file(json_data)
    return processed_text

# Initialize the Ollama model
if 'llm' not in st.session_state:
    st.session_state.llm = Ollama(
        base_url="http://localhost:11434",
        model="llama3.1",
        verbose=True,
        callback_manager=CallbackManager(
            [StreamingStdOutCallbackHandler()]
        )
    )

# Initialize session state for the JSON data
if 'json_text' not in st.session_state:
    st.session_state.json_text = load_and_process_json()

# Streamlit interface
st.title("AI assisstant")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to handle querying
def query_documents(query):
    if 'json_text' not in st.session_state:
        st.write("JSON data not initialized.")
        return "No data available for querying."

    json_text = st.session_state.json_text
    
    # Prepare the input for the Ollama model
    input_text = f"Given the following data: {json_text}\n\n{query}"
    
    try:
        # Query the Ollama model
        response = st.session_state.llm.predict(input_text)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

# Chat input
user_input = st.text_input("You:")

if user_input:
    user_message = {"role": "user", "message": user_input}
    st.session_state.chat_history.append(user_message)
    st.write(f"**You:** {user_input}")

    # Querying the document
    response = query_documents(user_input)

    chatbot_message = {"role": "assistant", "message": response}
    st.session_state.chat_history.append(chatbot_message)
    st.write(f"**Assistant:** {response}")
