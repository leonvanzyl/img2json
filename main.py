from dotenv import load_dotenv
load_dotenv()

import json

# Langchain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

# Retrieval imports
from langchain_community.document_loaders import S3DirectoryLoader
from langchain_community.document_loaders import S3FileLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader

def get_docs_from_folder(name):
    # if name (a file name) has extension .jpg or .png, then use UnstructuredImageLoader
    # else use S3DirectoryLoader
    loader = None
    if name.endswith('.jpg') or name.endswith('.png'):
        loader = UnstructuredImageLoader("lvz-img2json", name + "/")
    else:
        loader = S3DirectoryLoader("lvz-img2json", name + "/")

    docs = loader.load()
    return docs

def get_docs_from_file(name, fileName):
    loader = S3FileLoader("lvz-img2json", name + '/' + fileName)
    docs = loader.load()
    return docs

def process_input(name, user_input, uploaded_files):

    # create an empty list called docs and then loop through uploaded_files, 
    # then take the response from get_docs_from_file and append it to docs
    docs = []
    for file in uploaded_files:
        docs.extend(get_docs_from_file(name, file.name))

    # docs = get_docs_from_folder(name)
        
    print(docs)


    model = ChatOpenAI(
        model='gpt-3.5-turbo-1106'
    )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Generate a JSON response based on the schema provided by the user, and by extracting the information from the context.  Stick to the schema provided by the user. Do NOT include ```json at the start of the response or ``` at the end of the response."),
        ("human", "{context}"),
        ("human", "Populate the following schema: {input}")
    ]
    )

    # Create Stuff Chain
    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt,
    )

    

    # Invoke chain
    response = chain.invoke({
        "input": user_input,
        "context": docs
    })

    print(response)
    return response

if __name__ == "__main__":
    process_input()