from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import pandas as pd
from google.cloud import storage
import os
import configparser
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/teekyboy/code/gcp/chatbot-t1-firebase.json'
config = configparser.ConfigParser()
config.read('../config.ini')
OPENAI_API_KEY = config.get('api_key', 'openai')
PINECONE_API_KEY = config.get('api_key', 'pinecone')
PINECONE_ENV = config.get('env', 'pinecone')
PINECONE_INDEX = config.get('index', 'pinecone')
index_name = PINECONE_INDEX
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)
index_name = PINECONE_INDEX

db = Pinecone.from_existing_index(index_name, embeddings)

def run_query(user_input, db, OPENAI_API_KEY):
    llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
    answer = qa.run(user_input)
    return answer

def log_question_answer(query, answer):
    prefix = 'data/output/'
    log_file = f'{prefix}questions_answers.csv'
    bucket_name = 'chatbot-t1.appspot.com'
    data = {'question': [query], 'answer': [answer]}
    df = pd.DataFrame(data)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = storage.Blob(log_file, bucket)
    if blob.exists():
        content = blob.download_as_text()
        existing_df = pd.read_csv(io.StringIO(content))
        new_df = existing_df.append(df, ignore_index=True)
    else:
        new_df = df
    new_content = new_df.to_csv(index=False)
    blob.upload_from_string(new_content, content_type='text/csv')
