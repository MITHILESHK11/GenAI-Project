import streamlit as st
import os
from utils import initialize_session_state
from agent import (
    summarize_text,
    answer_question,
    generate_study_tips,
    check_api_key
)

# App title and description
st.set_page_config(
    page_title="Gemini-Powered Student Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Sidebar for API key
with st.sidebar:
    st.title("📚 Student Assistant")
    
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        value=st.session_state.get("api_key", os.getenv("GEMINI_API_KEY", "")),
        help="Get your API key from https://ai.google.dev/"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        api_status = check_api_key(api_key)
        if api_status:
            st.success("API Key is valid!")
        else:
            st.error("Invalid API Key. Please check and try again.")
    
    st.markdown("---")
    st.markdown("""
    ### About
    This app helps students with:
    - Summarizing notes
    - Answering questions
    - Providing study tips
    
    Powered by Google's Gemini API.
    """)

# Main content
st.title("Gemini-Powered Student Assistant")
st.markdown("Your AI study companion for note summarization, Q&A, and study tips.")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📝 Summarize Notes", "❓ Answer Questions", "💡 Study Tips"])

# Summarize Notes tab
with tab1:
    st.header("Summarize Your Notes")
    st.markdown("Paste your notes below and get a concise summary to aid your studying.")
    
    notes_text = st.text_area(
        "Your Notes",
        height=200,
        placeholder="Paste your notes or text here to summarize...",
        key="notes_input"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        summarize_button = st.button("Summarize", use_container_width=True)
    with col2:
        summary_length = st.select_slider(
            "Summary Length",
            options=["Very Short", "Short", "Medium", "Detailed"],
            value="Medium"
        )
    
    if summarize_button and notes_text:
        if not st.session_state.get("api_key"):
            st.error("Please enter your Gemini API Key in the sidebar.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    summary = summarize_text(notes_text, summary_length, st.session_state.api_key)
                    st.session_state.last_summary = summary
                    st.success("Summary generated!")
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")
                    summary = None
            
            if summary:
                st.markdown("### Summary")
                st.markdown(summary)
                st.markdown("---")
                
                # Add to history
                if "history" not in st.session_state:
                    st.session_state.history = []
                
                history_item = {
                    "type": "summary",
                    "input": notes_text[:100] + "..." if len(notes_text) > 100 else notes_text,
                    "output": summary[:100] + "..." if len(summary) > 100 else summary
                }
                st.session_state.history.insert(0, history_item)

# Answer Questions tab
with tab2:
    st.header("Ask Academic Questions")
    st.markdown("Ask any academic question and get a detailed answer to help with your studies.")
    
    # Option to use last summary as context
    use_summary_context = False
    if st.session_state.get("last_summary"):
        use_summary_context = st.checkbox("Use my last summary as context for better answers")
    
    question = st.text_input(
        "Your Question",
        placeholder="E.g., What are the key factors that led to World War II?",
        key="question_input"
    )
    
    subject_area = st.selectbox(
        "Subject Area (Optional)",
        ["General", "Mathematics", "Science", "History", "Literature", "Computer Science", 
         "Economics", "Philosophy", "Arts", "Social Sciences"]
    )
    
    if st.button("Get Answer", use_container_width=False):
        if not question:
            st.warning("Please enter a question first.")
        elif not st.session_state.get("api_key"):
            st.error("Please enter your Gemini API Key in the sidebar.")
        else:
            context = st.session_state.last_summary if use_summary_context else None
            
            with st.spinner("Thinking..."):
                try:
                    answer = answer_question(question, subject_area, context, st.session_state.api_key)
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    answer = None
            
            if answer:
                st.markdown("### Answer")
                st.markdown(answer)
                
                # Add to history
                if "history" not in st.session_state:
                    st.session_state.history = []
                
                history_item = {
                    "type": "question",
                    "input": question,
                    "output": answer[:100] + "..." if len(answer) > 100 else answer
                }
                st.session_state.history.insert(0, history_item)

# Study Tips tab
with tab3:
    st.header("Get Personalized Study Tips")
    st.markdown("Get personalized study tips and strategies based on your specific needs.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input(
            "Subject/Topic",
            placeholder="E.g., Organic Chemistry, Calculus, World History",
            key="subject_input"
        )
    
    with col2:
        goal = st.selectbox(
            "Study Goal",
            ["Exam Preparation", "Long-term Retention", "Understanding Complex Concepts", 
             "Improving Focus", "Time Management", "Note-taking", "Memory Improvement"]
        )
    
    learning_style = st.selectbox(
        "Your Learning Style (Optional)",
        ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Not Sure"]
    )
    
    additional_info = st.text_area(
        "Additional Information (Optional)",
        placeholder="Any specific challenges or preferences you have when studying this subject...",
        height=100
    )
    
    if st.button("Generate Study Tips", use_container_width=False):
        if not subject:
            st.warning("Please enter a subject first.")
        elif not st.session_state.get("api_key"):
            st.error("Please enter your Gemini API Key in the sidebar.")
        else:
            with st.spinner("Generating personalized study tips..."):
                try:
                    tips = generate_study_tips(subject, goal, learning_style, additional_info, st.session_state.api_key)
                except Exception as e:
                    st.error(f"Error generating study tips: {str(e)}")
                    tips = None
            
            if tips:
                st.markdown("### Your Personalized Study Tips")
                st.markdown(tips)
                
                # Add to history
                if "history" not in st.session_state:
                    st.session_state.history = []
                
                history_item = {
                    "type": "study_tips",
                    "input": f"Subject: {subject}, Goal: {goal}",
                    "output": tips[:100] + "..." if len(tips) > 100 else tips
                }
                st.session_state.history.insert(0, history_item)

# Display history at the bottom
if st.session_state.get("history"):
    st.markdown("---")
    with st.expander("📜 History", expanded=False):
        for i, item in enumerate(st.session_state.history[:10]):  # Show last 10 interactions
            st.markdown(f"**{item['type'].title()}**: {item['input']}")
            st.markdown(f"**Response**: {item['output']}")
            if i < len(st.session_state.history[:10]) - 1:
                st.markdown("---")
        
        if len(st.session_state.history) > 10:
            st.markdown(f"*{len(st.session_state.history) - 10} more interactions not shown*")
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
