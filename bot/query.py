import os
import configparser
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def load_config():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config.get('api_key', 'openai')

def load_faiss_db(vector_directory, embeddings):
    return FAISS.load_local(vector_directory, embeddings)

def initialize_qa_chain(llm, retriever):
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

def ask_question(qa, query):
    return qa.run(query)

def answer_question(user_input):
    vector_directory = "../data/embeddings/"
    OPENAI_API_KEY = load_config()
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = load_faiss_db(vector_directory, embeddings)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    qa = initialize_qa_chain(llm, vectordb.as_retriever())

    response = ask_question(qa, user_input)
    return response

def log_question_answer(user_input, answer):
    log_file = '../data/output/questions_answers.csv'
    data = {'question': [user_input], 'answer': [answer]}

    df = pd.DataFrame(data)
    if not os.path.isfile(log_file):
        df.to_csv(log_file, index=False)
    else:
        df.to_csv(log_file, mode='a', header=False, index=False)
