import streamlit as st

from components import sidebar
from components.chatbot import ChatBot
from components.vector_db import VectorDB, get_vector_db

# Configure Streamlit page
st.set_page_config(page_title="SQL tasks lookup", page_icon="🤖", layout="wide")

# Set assistant and user avatars
assistant_avatar = "🤖"
user_avatar = "🤷‍♂️"

# Initialize sidebar
sidebar.init_sidebar()

# Set app title and logo
st.title("SQL tasks lookup")

# Initialize VectorDB
vector_db: VectorDB = get_vector_db()
chatbot = ChatBot()

# Set up the input field
with st.form("sector_lookup"):
    user_input = st.text_area("Enter a business industry description:", height=150)
    st.form_submit_button("Look up SQL tasks examples.")

# Check if the user has entered a description
if user_input:
    with st.spinner("Processing..."):
        # Get a table of the most similar sectors
        st.session_state.retrieved_context = vector_db(user_input)
        st.session_state.retrieved_data = vector_db.query_table(user_input)

    st.write("### Results for the Retrieval phase:")
    st.table(st.session_state.retrieved_data)

    with st.spinner("Generating SQL tasks..."):
        chatbot_response = chatbot.invoke(user_input, st.session_state.retrieved_context)

    st.write("### Results for the Generation phase:")
    st.markdown(chatbot_response)