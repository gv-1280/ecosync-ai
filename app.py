import streamlit as st
import base64
import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from agent_flow import enhanced_app_flow  # Updated flow

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
        page_title="Ecosync AI - Multi-Agent Environmental & Health System",
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
        .health-card {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: #333;
            margin-bottom: 1rem;
        }
        .clinic-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #ff6b6b;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with full width
    st.title("🌍 Ecosync AI - Multi-Agent Environmental & Health System")
    st.subheader("Supporting UN SDGs 14, 15, and 3 with Health-Aware Environmental Analysis")
    
    # Create main layout with sidebar and main content
    with st.sidebar:
        st.header("🎯 Intelligent Agent System")
        st.markdown("""
        **🤖 Available Agents:**
        
        🌍 **Eco Chatbot Agent**
        - Environmental Q&A
        - Human health + environment
        - Climate & conservation
        
        🌊 **Marine Health Agent** 
        - Ocean ecosystem analysis
        - Marine life health
        - Water quality & human impact
        
        🌳 **Land Health Agent**
        - Terrestrial wildlife analysis
        - Air quality assessment
        - Land-based health impacts
        """)
        
        st.markdown("---")
        st.markdown("### 🏥 Health Integration")
        st.markdown("""
        **NEW: Health-Aware Analysis**
        - Detects human health queries
        - Links environmental & human health
        - Suggests nearby clinics
        - Environmental health risks
        """)
        
        st.markdown("---")
        st.markdown("**💡 Query Examples:**")
        st.info("""
        • "Is this water safe to swim in?"
        • "Air pollution effects on health"
        • "Coral bleaching health impacts"
        • "Forest fire smoke exposure"
        • "I have a rash after beach visit"
        """)
    
    # Main content area - wider layout
    main_col1, main_col2 = st.columns([2, 1], gap="large")
    
    with main_col1:
        st.markdown("### 💬 Ask Your Environmental or Health Question")
        user_input = st.text_area(
            "Enter your question or describe what you'd like to analyze:",
            placeholder="Examples:\n• 'I have breathing issues from air pollution - what should I know?'\n• 'Is this coral reef showing signs of bleaching?'\n• 'Water contamination effects on human health'\n• 'Wildlife disease that could affect humans'",
            height=150,
            key="main_input"
        )
        
        # City input for health-related queries
        st.markdown("### 📍 Location (For Health Recommendations)")
        user_city = st.text_input(
            "Enter your city name (optional - for nearby clinic suggestions):",
            placeholder="e.g., Delhi, Mumbai, Bangalore, Gurugram",
            help="Providing your city helps us suggest nearby healthcare facilities for health-related queries"
        )
        
        st.markdown("### 📸 Upload Image (Optional)")
        uploaded_file = st.file_uploader(
            "Choose an image for analysis:",
            type=['png', 'jpg', 'jpeg'],
            help="Marine life, coral reefs, forests, wildlife, environmental conditions, or health-related images",
            key="image_upload"
        )
        
        # Large, prominent analyze button
        analyze_button = st.button("🔍 Analyze with AI Health-Aware Agents", type="primary", key="analyze_btn")
    
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
            st.markdown("""
            <div class="health-card">
                <h4>🏥 Health-Aware Analysis</h4>
                <p>Our system now detects health-related queries and provides:</p>
                <ul>
                    <li>Environmental health connections</li>
                    <li>Nearby healthcare facilities</li>
                    <li>Safety recommendations</li>
                    <li>When to seek medical help</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **📊 Analysis Types:**
            - 🐠 Marine ecosystem + water safety
            - 🪸 Coral health + tourism safety  
            - 🌊 Water pollution + health risks
            - 🦅 Wildlife health + disease vectors
            - 🌲 Forest health + air quality
            - 🍃 Environmental toxins + human impact
            """)
    
    # Process analysis with full-width results
    if analyze_button:
        if not user_input.strip():
            st.error("Please enter a question or description.")
            return
        
        # Full width processing section
        st.markdown("---")
        
        with st.spinner("🤖 Processing with Health-Aware AI agents..."):
            try:
                # Invoke the enhanced LangGraph flow
                result = enhanced_app_flow.invoke({
                    "input": user_input,
                    "image": img_base64,
                    "user_city": user_city.strip() if user_city else ""
                })
                
                # Extract response and metadata
                response = result.get("response", "No response generated.")
                metadata = result.get("metadata", {})
                clinic_data = result.get("clinic_data", [])
                health_type = result.get("health_type", "environmental")
                agent_used = metadata.get("agent_used", "Unknown")
                
                # Results section with full width layout
                st.success(f"✅ Analysis Complete - **{agent_used.replace('_', ' ').title()}** ({health_type} analysis)")
                
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
                    
                    # Health type indicator
                    health_colors = {
                        "human": "🏥",
                        "environmental_marine": "🌊",
                        "environmental_land": "🌿",
                        "marine": "🐠",
                        "land": "🌳",
                        "environmental": "🌍"
                    }
                    
                    st.info(f"**Analysis Type:** {health_colors.get(health_type, '🔍')} {health_type.replace('_', ' ').title()}")
                    
                    # Agent selection info
                    if "routing_reason" in metadata:
                        st.text(metadata["routing_reason"])
                    
                    # Processing details
                    st.markdown("**Processing Info:**")
                    st.write(f"🖼️ Image: {'✅ Yes' if img_base64 else '❌ No'}")
                    st.write(f"📍 City: {'✅ ' + user_city if user_city else '❌ Not provided'}")
                    st.write(f"🏥 Health Focus: {'✅ Yes' if health_type in ['human', 'environmental_marine', 'environmental_land'] else '❌ No'}")
                    
                    if metadata.get("success") is False and "error" in metadata:
                        st.error(f"⚠️ Error: {metadata['error']}")
                
                # Clinic suggestions section (if available)
                if clinic_data:
                    st.markdown("---")
                    st.markdown("### 🏥 Nearby Healthcare Facilities")
                    
                    clinic_cols = st.columns(min(len(clinic_data), 3))
                    
                    for idx, clinic in enumerate(clinic_data[:3]):
                        with clinic_cols[idx % 3]:
                            st.markdown(f"""
                            <div class="clinic-card">
                                <h4>🏥 {clinic['name']}</h4>
                                <p><strong>📍 Address:</strong><br>{clinic['address']}</p>
                                <p><strong>📞 Phone:</strong> {clinic.get('phone', 'Contact local directory')}</p>
                                {f"<p><strong>⭐ Rating:</strong> {clinic['rating']}/5</p>" if clinic.get('rating') != 'N/A' else ""}
                                {f"<p><strong>🌐 Website:</strong> <a href='{clinic['website']}' target='_blank'>Visit</a></p>" if clinic.get('website') else ""}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Health disclaimer for medical queries
                if health_type in ["human", "environmental_marine", "environmental_land"]:
                    st.markdown("---")
                    st.warning("""
                    ⚠️ **Medical Disclaimer**: This AI provides educational information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.
                    """)
                
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
        - OpenStreetMap (Clinic Data)
        """)
    
    with footer_col3:
        st.markdown("""
        **🔗 Resources:**
        - [OpenRouter API](https://openrouter.ai)
        - [WHO Health Info](https://www.who.int)
        - [Environmental Health](https://www.cdc.gov/environmental-health/)
        """)

if __name__ == "__main__":
    main()