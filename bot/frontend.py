import streamlit as st
from query import run_query, log_question_answer
import os
import configparser
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/teekyboy/code/gcp/chatbot-t1-firebase.json'
config = configparser.ConfigParser()
config.read('../config.ini')
OPENAI_API_KEY = config.get('api_key', 'openai')
PINECONE_API_KEY = config.get('api_key', 'pinecone')
PINECONE_ENV = config.get('env', 'pinecone')
PINECONE_INDEX = config.get('index', 'pinecone')
index_name = PINECONE_INDEX
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db = Pinecone.from_existing_index(index_name, embeddings)


def main():
    st.title("Question Answering")
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
