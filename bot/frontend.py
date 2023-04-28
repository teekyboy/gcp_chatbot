import streamlit as st
from query import answer_question, log_question_answer

def main():
    st.title("Question Answering")
    st.subheader("Ask Questions")
    user_input = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_input:
            answer = answer_question(user_input)
            st.write(answer)
            log_question_answer(user_input, answer)
        else:
            st.error("Please enter a question before submitting.")

if __name__ == "__main__":
    main()
