import streamlit as st
from query import run_query, log_question_answer
import os
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from google.cloud import secretmanager_v1

os.environ['GOOGLE_CLOUD_PROJECT'] = 'chatbot-t1'

def get_secret(secret_id):
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode('UTF-8')

#for cloud run
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/chatbot-t1-firebase.json'
#for local run
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../chatbot-t1-firebase.json'
OPENAI_API_KEY = get_secret('openai_api_key')
PINECONE_API_KEY = get_secret('pinecone_api_key')
PINECONE_ENV = get_secret('pinecone_env')
PINECONE_INDEX = get_secret('pinecone_index')
index_name = PINECONE_INDEX
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db = Pinecone.from_existing_index(index_name, embeddings)

def main():
    st.title("What do you want to know?")
    st.subheader("Ask Questions")
    user_input = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_input:
            answer = run_query(user_input, db, OPENAI_API_KEY)
            st.write(answer)
            log_question_answer(user_input, answer)
        else:
            st.error("Please enter a question before submitting.")

if __name__ == "__main__":
    main()
