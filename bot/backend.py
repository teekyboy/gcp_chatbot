import streamlit as st
from create import upload_and_create

def main():
    st.title("Upload Files")
    uploaded_files = st.file_uploader("Choose Files to Upload", accept_multiple_files=True)

    if uploaded_files:
        if upload_and_create(uploaded_files):
            st.success("Database created and saved!")
        else:
            st.error("Error creating database.")

if __name__ == "__main__":
    main()
