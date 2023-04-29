import os
from google.cloud import storage
import streamlit as st
import pinecone
from create import load_documents
from langchain.vectorstores import Pinecone

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../chatbot-t1-firebase.json'

def upload_file_to_gcs(uploaded_file, folder_prefix):
    storage_client = storage.Client()
    bucket_name = "chatbot-t1.appspot.com"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(f"{folder_prefix}/{uploaded_file.name}")
    blob.upload_from_string(uploaded_file.getvalue(), content_type=uploaded_file.type)

def create_database(docs, embeddings, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX):
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    index_name = PINECONE_INDEX
    db = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    return db

def app():
    st.title("Create Database")
    uploaded_file = st.file_uploader("Choose a file to upload", type=['txt', 'pdf', 'doc', 'docx'])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        if st.button("Upload and Process Documents"):
            folder_prefix = "data/input"
            upload_file_to_gcs(uploaded_file, folder_prefix)
            docs, embeddings, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX = load_documents()
            db = create_database(docs, embeddings, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX)
            st.success("Database created successfully.")

if __name__ == "__main__":
    app()
