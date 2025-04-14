import streamlit as st
from utils.agent_helpers import query_race_agent

st.set_page_config(page_title="Chatbot | F1 Monza", page_icon="🏎️", layout="wide")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🗣️ Ask a Question")
    user_question = st.chat_input("Type your F1 question about Monza 2024 here...")

    if user_question:
        try:
            response, trace = query_race_agent(user_question)
            st.chat_message("user").write(user_question)
            st.chat_message("assistant").write(response)
        except Exception as e:
            st.error(f"An error occurred while querying the chatbot: {e}")
            trace = "No trace available due to error."

with col2:
    st.markdown("### 🧾 Traceability")
    if user_question and trace and trace != "Trace not available in this version.":
        if isinstance(trace, list):
            for i, item in enumerate(trace):
                st.markdown(f"**Source {i+1}:** {item.get('source', 'Unknown source')}")
        else:
            st.code(trace, language="text")
    elif user_question:
        st.info("No traceability info returned for this query.")
    else:
        st.info("Ask a question to see SQL or source citations here.")
