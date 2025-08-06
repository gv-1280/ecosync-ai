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
    # Set wide layout and custom CSS for better laptop experience
    st.set_page_config(
        page_title="Ecosync AI - Multi-Agent Environmental System",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better laptop UI
    st.markdown("""
    <style>
        .main > div {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-size: 1.2rem;
        }
        .agent-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1rem;
        }
        .usage-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1rem;
        }
        .feature-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with full width
    st.title("🌍 Ecosync AI - Multi-Agent Environmental System")
    st.subheader("Supporting UN SDGs 14 (Life Below Water), 15 (Life on Land), and 3 (Good Health and Well-being)")
    
    # Create main layout with sidebar and main content
    with st.sidebar:
        st.header("🎯 Agent Selection")
        st.markdown("""
        **Available Agents:**
        
        🌍 **Eco Chatbot Agent**
        - General environmental Q&A
        - Climate change information
        - Conservation strategies
        
        🌊 **Marine Health Agent** 
        - Ocean life analysis
        - Marine ecosystem health
        - Coral reef assessment
        
        🌳 **Land Health Agent**
        - Terrestrial wildlife analysis  
        - Forest ecosystem health
        - Animal behavior insights
        """)
        
        st.markdown("---")
        st.markdown("**💡 Tips for Better Results:**")
        st.info("""
        • Be specific in your questions
        • Upload high-quality images
        • Mention the type of analysis needed
        • Include location context if relevant
        """)
    
    # Main content area - wider layout
    main_col1, main_col2 = st.columns([2, 1], gap="large")
    
    with main_col1:
        st.markdown("### 💬 Ask Your Environmental Question")
        user_input = st.text_area(
            "Enter your question or describe what you'd like to analyze:",
            placeholder="Examples:\n• 'What are the signs of coral bleaching in this image?'\n• 'How can communities help marine conservation?'\n• 'Analyze the health of this forest ecosystem'\n• 'What threats do polar bears face due to climate change?'",
            height=150,
            key="main_input"
        )
        
        st.markdown("### 📸 Upload Image (Optional)")
        uploaded_file = st.file_uploader(
            "Choose an image for marine or terrestrial analysis:",
            type=['png', 'jpg', 'jpeg'],
            help="Supported: Marine life, coral reefs, forests, wildlife, ecosystems",
            key="image_upload"
        )
        
        # Large, prominent analyze button
        analyze_button = st.button("🔍 Analyze with AI Agents", type="primary", key="analyze_btn")
    
    with main_col2:
        st.markdown("### 🖼️ Image Preview")
        img_base64 = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            img_base64 = encode_image_to_base64(image)
            
            # Image info
            st.markdown(f"""
            **Image Details:**
            - Size: {image.size[0]}x{image.size[1]} pixels
            - Format: {image.format}
            - Mode: {image.mode}
            """)
        else:
            st.info("Upload an image to see preview here")
            st.markdown("""
            **Supported Analysis:**
            - 🐠 Marine species identification
            - 🪸 Coral health assessment  
            - 🌊 Ocean pollution detection
            - 🦅 Wildlife behavior analysis
            - 🌲 Forest health monitoring
            - 🍃 Ecosystem biodiversity
            """)
    
    # Process analysis with full-width results
    if analyze_button:
        if not user_input.strip():
            st.error("Please enter a question or description.")
            return
        
        # Full width processing section
        st.markdown("---")
        
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
                
                # Results section with full width layout
                st.success(f"✅ Analysis Complete - **{agent_used.replace('_', ' ').title()}** was used")
                
                # Two-column results layout
                result_col1, result_col2 = st.columns([3, 1], gap="large")
                
                with result_col1:
                    st.markdown("### 🎯 Analysis Results:")
                    st.markdown(f"""
                    <div style="background-color: #f0f8ff; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #4CAF50;">
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col2:
                    st.markdown("### 📊 Analysis Details")
                    
                    # Agent selection info
                    if "routing_reason" in metadata:
                        st.info(f"**Agent Selected:** {agent_used.replace('_', ' ').title()}")
                        st.text(metadata["routing_reason"])
                    
                    # Processing details
                    st.markdown("**Processing Info:**")
                    st.write(f"🖼️ Image: {'✅ Yes' if img_base64 else '❌ No'}")
                    st.write(f"🤖 Model: {metadata.get('model', 'N/A')}")
                    st.write(f"✅ Success: {'Yes' if metadata.get('success', True) else 'No'}")
                    
                    if metadata.get("success") is False and "error" in metadata:
                        st.error(f"⚠️ Error: {metadata['error']}")
                
                # Additional insights section (full width)
                st.markdown("---")
                insight_col1, insight_col2, insight_col3 = st.columns(3, gap="medium")
                
                with insight_col1:
                    st.markdown("""
                    <div class="feature-card">
                        <h4>🌊 Marine Conservation</h4>
                        <p>Learn about ocean protection strategies and marine ecosystem health monitoring.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with insight_col2:
                    st.markdown("""
                    <div class="feature-card">
                        <h4>🌳 Land Conservation</h4>
                        <p>Discover wildlife protection methods and terrestrial habitat preservation.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with insight_col3:
                    st.markdown("""
                    <div class="feature-card">
                        <h4>🌍 Climate Action</h4>
                        <p>Explore climate change solutions and environmental sustainability practices.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"🚨 An error occurred: {str(e)}")
                st.error("Please check your configuration and try again.")
                
                # Error details in expandable section
                with st.expander("🔍 View Error Details"):
                    st.code(str(e))
    
    # Footer section with full width
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.markdown("""
        **🎯 UN SDG Goals:**
        - SDG 14: Life Below Water
        - SDG 15: Life on Land  
        - SDG 3: Good Health and Well-being
        """)
    
    with footer_col2:
        st.markdown("""
        **🤖 AI Models:**
        - Mistral Small 3.2 (Text Analysis)
        - Kimi Vision A3B (Image Analysis)
        - LangGraph Multi-Agent Routing
        """)
    
    with footer_col3:
        st.markdown("""
        **🔗 Resources:**
        - [OpenRouter API](https://openrouter.ai)
        - [UN SDGs](https://sdgs.un.org)
        - [Environmental Data](https://www.unep.org)
        """)
    
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-top: 2rem;'>
        <h3>🌱 Ecosync AI - Powered by Multi-Agent Intelligence for Environmental Conservation</h3>
        <p>Leveraging AI to support global environmental protection and sustainability initiatives</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()