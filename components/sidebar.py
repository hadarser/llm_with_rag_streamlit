"""Create the sidebar for the app."""
import streamlit as st

def init_sidebar():
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/87/Sql_data_base_with_logo.png")
        st.markdown("---")
        st.markdown("How to:")
        st.markdown(
            "📁 Look up for a business sector."
            "Write the best description you can think of and I will find the SQL tasks relevant this sector 📌"
        )

        # Placeholder for process spinner
        st.markdown("---")
        st.session_state["process_spinner"] = st.empty()