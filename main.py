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

def get_docs_from_folder(name):
    loader = S3DirectoryLoader("lvz-img2json", name + "/")
    docs = loader.load()
    print(docs)
    return docs

def get_docs_from_file(fileName):
    loader = S3FileLoader("lvz-img2json", fileName)

def process_input(name, user_input, uploaded_files):

    model = ChatOpenAI(
        model='gpt-3.5-turbo-1106'
    )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Generate a JSON response based on the schema provided by the user, and by extracting the information from the context.  Stick to the schema provided by the user."),
        ("human", "{context}"),
        ("human", "Populate the following schema: {input}")
    ]
    )

    # Create Stuff Chain
    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt,
    )

    docs = get_docs_from_folder(name)

    # Invoke chain
    response = chain.invoke({
        "input": user_input,
        "context": docs
    })

    print(response)
    return response

if __name__ == "__main__":
    process_input()