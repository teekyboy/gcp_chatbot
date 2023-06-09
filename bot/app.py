import streamlit as st
from backend import app as backend_app
from frontend import main as frontend_app

st.set_page_config(page_title="My App", page_icon=None, layout="wide", initial_sidebar_state="expanded")

def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("What do you want to do?", ["Load New Files" , "Test My Knowledge"])

    if app_mode == "Load New Files":
        backend_app()
    elif app_mode == "Test My Knowledge":
        frontend_app()


    add_custom_css()

def add_custom_css():
    custom_css = """
    <style>
        /* Set the background color for the entire app */
        body {
            background-color: #f5f5f5;
        }

        /* Set the background color and border for the sidebar */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }

        /* Set the font color and background color for the title in the sidebar */
        .sidebar .sidebar-content .block-container h1 {
            color: #ffffff;
            background-color: #4a90e2;
            padding: 10px 16px;
            margin-bottom: 10px;
        }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
