import json
import streamlit as st

JSON_FILE_PATH = r'C:\Users\monia.fawzi\Downloads\ai json\llama3-1\sample.json'

@st.cache_resource
def load_json():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            json_data = json.load(file)
            st.write("JSON data successfully loaded.")
            st.write(json_data)
    except Exception as e:
        st.write(f"An error occurred: {e}")

load_json()

