import streamlit as st

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if "last_summary" not in st.session_state:
        st.session_state.last_summary = None
