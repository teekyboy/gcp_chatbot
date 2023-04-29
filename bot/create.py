from langchain.document_loaders import GCSDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import configparser

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/teekyboy/code/gcp/chatbot-t1-firebase.json'

def load_documents():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/teekyboy/code/gcp/chatbot-t1-firebase.json'
    config = configparser.ConfigParser()
    config.read('../config.ini')
    OPENAI_API_KEY = config.get('api_key', 'openai')
    PINECONE_API_KEY = config.get('api_key', 'pinecone')
    PINECONE_ENV = config.get('env', 'pinecone')
    PINECONE_INDEX = config.get('index', 'pinecone')
    loader = GCSDirectoryLoader(project_name="chatbot", bucket="chatbot-t1.appspot.com", prefix="data/input")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return docs, embeddings, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX
