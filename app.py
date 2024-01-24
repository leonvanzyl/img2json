from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
import os

import boto3
from botocore.exceptions import NoCredentialsError

from main import process_input

# Your existing imports and functions...

def save_uploaded_file(uploaded_file, bucket_name):
    s3 = boto3.client('s3')

    try:
        # Convert the uploaded file to bytes
        file_content = uploaded_file.getbuffer().tobytes()
        
        # Create a unique file name if needed
        file_name = uploaded_file.name  # Modify as needed for unique naming

        # Upload the file
        s3.put_object(Bucket=bucket_name, Key=name + '/' + file_name, Body=file_content)
        return True
    except NoCredentialsError:
        st.error("AWS credentials not found")
        return False
    except Exception as e:
        st.error(f"Error uploading file to S3: {e}")
        return False

st.title("Img2JSON")

name = st.text_input("Enter your name", "")

# File uploader
uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True)
bucket_name = "lvz-img2json"
if uploaded_files:
    for uploaded_file in uploaded_files:
        if save_uploaded_file(uploaded_file, bucket_name):
            st.success(f"File uploaded successfully: {uploaded_file.name}")
        else:
            st.error("Error saving file to S3")

# Text input
            
placeholder_text = '''{
  "name": "the name of the person as string",
  "age": "the age of the person as number",
  "address": "the address of the person as a list"
}'''

user_input = st.text_area("Provide your JSON Schema", value=placeholder_text, height=300)

# Submit button
if st.button("Submit"):
    if name: 
        # Assuming your existing script's logic goes here
        # Modify your script to use 'user_input' and uploaded files

        # Display output
        response = process_input(name, user_input, uploaded_files)
        st.json(response)

        # Copy to clipboard button
        if st.button("Copy JSON to Clipboard"):
            st.sidebar.text_area("Copy to Clipboard:", response, height=300)
    else:
        st.error("Please enter your name to proceed.")