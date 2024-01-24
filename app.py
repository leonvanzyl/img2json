import streamlit as st
import json
import os

from main import process_input

# Your existing imports and functions...

def save_uploaded_file(uploaded_file):
    try:
        src_dir = 'src'
        if not os.path.exists(src_dir):
            os.makedirs(src_dir)

        with open(os.path.join("src", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except:
        return False

st.title("Img2JSON")

# File uploader
uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        if save_uploaded_file(uploaded_file):
            st.success(f"Saved file: {uploaded_file.name}")
        else:
            st.error("Error saving file")

# Text input
            
placeholder_text = '''{
  "name": "the name of the person as string",
  "age": "the age of the person as number",
  "address": "the address of the person as a list"
}'''

user_input = st.text_area("Provide your JSON Schema", value=placeholder_text, height=300)

# Submit button
if st.button("Submit"):
    # Assuming your existing script's logic goes here
    # Modify your script to use 'user_input' and uploaded files

    # Display output
    response = process_input(user_input)
    st.json(response)

    # Copy to clipboard button
    if st.button("Copy JSON to Clipboard"):
        st.sidebar.text_area("Copy to Clipboard:", response, height=300)
