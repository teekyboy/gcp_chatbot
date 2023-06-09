from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import pandas as pd
from google.cloud import storage
import os
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import io
from google.cloud import secretmanager_v1

os.environ['GOOGLE_CLOUD_PROJECT'] = 'chatbot'

def get_secret(secret_id):
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode('UTF-8')

#for cloud run
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/chatbot.json'
#for local run
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../chatbot.json'
OPENAI_API_KEY = get_secret('openai_api_key')
PINECONE_API_KEY = get_secret('pinecone_api_key')
PINECONE_ENV = get_secret('pinecone_env')
PINECONE_INDEX = get_secret('pinecone_index')
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
