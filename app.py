import streamlit as st
import base64
import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from agent_flow import app_flow

# Load environment variables
load_dotenv()

def encode_image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def main():
    st.title("🌍 Ecosync AI - Multi-Agent Environmental System")
    st.subheader("Supporting UN SDGs 14, 15, and 3")
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Available Agents:
        - 🌍 **Eco Chatbot**: General environmental Q&A
        - 🌊 **Marine Health**: Analyze ocean life and marine environments  
        - 🌳 **Land Health**: Analyze terrestrial wildlife and ecosystems
        """)
    
    with col2:
        st.markdown("""
        ### How to Use:
        1. Type your question
        2. Upload image (optional)
        3. Get AI-powered insights
        """)
    
    # Input section
    st.markdown("---")
    user_input = st.text_area(
        "Ask your environmental question:",
        placeholder="e.g., 'What are the signs of coral bleaching?' or 'How can I help marine conservation?'",
        height=100
    )
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload an image (optional - for marine/land analysis):",
        type=['png', 'jpg', 'jpeg'],
        help="Upload images of marine life, land animals, or ecosystems for detailed analysis"
    )
    
    # Process and display uploaded image
    img_base64 = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        img_base64 = encode_image_to_base64(image)
    
    # Submit button
    if st.button("🔍 Analyze", type="primary"):
        if not user_input.strip():
            st.error("Please enter a question or description.")
            return
        
        with st.spinner("🤖 Processing with Ecosync AI agents..."):
            try:
                # Invoke the LangGraph flow
                result = app_flow.invoke({
                    "input": user_input,
                    "image": img_base64
                })
                
                # Extract response and metadata
                response = result.get("response", "No response generated.")
                metadata = result.get("metadata", {})
                agent_used = metadata.get("agent_used", "Unknown")
                
                # Display results
                st.markdown("---")
                st.success(f"✅ Response from **{agent_used.replace('_', ' ').title()}**")
                
                # Show which agent was selected and why
                if "routing_reason" in metadata:
                    with st.expander("🧠 Agent Selection Details"):
                        st.info(metadata["routing_reason"])
                        if "has_image" in metadata:
                            st.write(f"Image provided: {'✅ Yes' if metadata['has_image'] else '❌ No'}")
                
                # Display the main response
                st.markdown("### 🎯 Analysis Results:")
                st.write(response)
                
                # Show additional metadata if available
                if metadata.get("success") is False and "error" in metadata:
                    st.error(f"Error occurred: {metadata['error']}")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please check your configuration and try again.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌱 Ecosync AI - Powered by Multi-Agent Intelligence for Environmental Conservation</p>
        <p>Supporting UN Sustainable Development Goals 14, 15, and 3</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()