import os
import configparser
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader

def load_config():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config.get('api_key', 'openai')

def load_and_process_documents(loader):
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    return text_splitter.split_documents(data)

def initialize_faiss_db(texts, embeddings):
    return FAISS.from_documents(documents=texts, embedding=embeddings)

def save_faiss_db(vectordb, vector_directory):
    vectordb.save_local(vector_directory)

def upload_and_create(uploaded_files):
    loader = DirectoryLoader("../data/input/")
    vector_directory = "../data/embeddings/"
    OPENAI_API_KEY = load_config()

    if uploaded_files:
        for file in uploaded_files:
            with open(os.path.join("../data/input/", file.name), "wb") as f:
                f.write(file.getbuffer())

        texts = load_and_process_documents(loader)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectordb = initialize_faiss_db(texts, embeddings)
        save_faiss_db(vectordb, vector_directory)
        return True
    return False
