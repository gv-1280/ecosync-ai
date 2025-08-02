import streamlit as st
from graph.agent_flow import run_agent_flow

st.set_page_config(page_title="Ecosync AI", layout="wide")

st.title("🤖 Welcome to Ecosync AI")
st.markdown("### 🌱 Ask me anything about the ocean, forests, marine health, or biodiversity.")

user_input = st.text_input("Type your question or concern below:")

if user_input:
    response = run_agent_flow(user_input)
    st.markdown("### 🧠 Ecosync Response")
    st.markdown(f"<div style='font-size:20px'>{response.get('response')}</div>", unsafe_allow_html=True)
