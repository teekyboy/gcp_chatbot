from langchain.document_loaders import GCSDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from google.cloud import secretmanager_v1

os.environ['GOOGLE_CLOUD_PROJECT'] = 'chatbot-t1'

def get_secret(secret_id):
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode('UTF-8')

def load_documents():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../chatbot-t1-firebase.json'
    OPENAI_API_KEY = get_secret('openai_api_key')
    PINECONE_API_KEY = get_secret('pinecone_api_key')
    PINECONE_ENV = get_secret('pinecone_env')
    PINECONE_INDEX = get_secret('pinecone_index')
    loader = GCSDirectoryLoader(project_name="chatbot", bucket="chatbot-t1.appspot.com", prefix="data/input")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return docs, embeddings, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX
