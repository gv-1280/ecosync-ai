import streamlit as st
from agent_flow import app_flow
import base64

st.set_page_config(page_title="EcoSync AI", page_icon="🌍", layout="centered")

st.title("🌱 EcoSync AI")
st.write("Empowering sustainability through intelligent agents. Ask a question or upload an image related to environment, marine life, or land health.")

# User input
user_input = st.text_area("Enter your query:", placeholder="e.g. What are the threats to coral reefs?", height=100)

# Image upload (optional)
uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

# Convert image to base64 if uploaded
img_base64 = None
if uploaded_image:
    img_bytes = uploaded_image.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

# Run Agent
if st.button("Ask Ecosync AI"):
    with st.spinner("Thinking..."):
        response = app_flow.invoke({
            "input": user_input,
            "image": img_base64
        })
        st.success("Response:")
        st.write(response.get("output", "No response"))
