import os
import streamlit as st
import httpx
import asyncio
import json
from typing import List, Optional, Dict, Any

# Configure page with modern settings
st.set_page_config(
    page_title="Divine Mirror AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS styling for AI-driven app
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Modern AI header */
    .ai-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .ai-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.1;
    }
    
    .ai-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    /* Modern glassmorphism containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Modern input styling */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        background: rgba(0, 0, 0, 0.6) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    
    /* Modern selectbox styling */
    .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    .stMultiSelect > div > div {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect > div > div > div {
        color: #ffffff !important;
    }
    
    /* Fix dropdown options */
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(0, 0, 0, 0.8) !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div {
        background: rgba(0, 0, 0, 0.8) !important;
        color: #ffffff !important;
    }
    
    /* Modern button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3) !important;
        text-transform: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* AI response container */
    .ai-response {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        border-left: 4px solid #667eea;
    }
    
    /* Modern metrics */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        margin: 0.25rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    .status-success {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .status-loading {
        background: rgba(249, 115, 22, 0.1);
        color: #f97316;
        border: 1px solid rgba(249, 115, 22, 0.2);
    }
    
    /* Modern text styling */
    .modern-text {
        color: #e2e8f0;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .modern-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-flex;
        gap: 0.3rem;
        margin-left: 0.5rem;
    }
    
    .loading-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #667eea;
        animation: loading 1.4s ease-in-out infinite both;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    .loading-dot:nth-child(3) { animation-delay: 0s; }
    
    @keyframes loading {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1.2); opacity: 1; }
    }
    
    /* Modern scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.5);
    }
    
    /* Modern sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Modern expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 0 12px 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Constants
API_BASE_URL = "http://localhost:8000"

# Session state initialization
if "query_results" not in st.session_state:
    st.session_state.query_results = None
if "selected_traditions" not in st.session_state:
    st.session_state.selected_traditions = []
if "comparison_mode" not in st.session_state:
    st.session_state.comparison_mode = "modern_vs_original"
if "time_periods" not in st.session_state:
    st.session_state.time_periods = []
if "sources" not in st.session_state:
    st.session_state.sources = []
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# API functions
async def query_spiritual_truth(question, traditions, comparison_mode, time_periods=None):
    """Send a query to the backend API and retrieve results"""
    if not time_periods:
        time_periods = []
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/query",
                json={
                    "question": question,
                    "traditions": traditions,
                    "comparison_mode": comparison_mode,
                    "time_periods": time_periods
                },
                timeout=120.0
            )
            return response.json()
        except httpx.RequestError as e:
            return {"error": f"Connection error: {e}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}

async def get_available_traditions():
    """Retrieve available religious traditions from the backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/traditions", timeout=30.0)
            return response.json()
        except Exception as e:
            return {"traditions": ["Christianity", "Buddhism", "Islam", "Judaism", "Taoism", "Hermeticism", "Gnosticism"]}

async def get_time_periods():
    """Retrieve available time periods from the backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/time_periods", timeout=30.0)
            return response.json()
        except Exception as e:
            return {"time_periods": ["Ancient (3000-500 BCE)", "Classical (500 BCE-500 CE)", "Contemporary (1800-Present)"]}

def main():
    # Modern header with AI branding
    st.markdown("""
    <div class="ai-header">
        <h1>🔮 Divine Mirror AI</h1>
        <p class="ai-subtitle">Unveiling Spiritual Truth Through Ancient Wisdom</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">91</div>
            <div class="metric-label">Sacred Texts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">76</div>
            <div class="metric-label">Bible Books</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">7</div>
            <div class="metric-label">Traditions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">∞</div>
            <div class="metric-label">Truth Revealed</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main interface in glassmorphism container
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Get available options
    def get_traditions():
        return asyncio.run(get_available_traditions())
    
    def fetch_time_periods():
        return asyncio.run(get_time_periods())
    
    traditions_data = get_traditions()
    time_periods_data = fetch_time_periods()
    
    available_traditions = traditions_data.get("traditions", [])
    available_time_periods = time_periods_data.get("time_periods", [])
    
    # Query interface
    st.markdown('<p class="modern-subtitle">🔍 Ask Your Spiritual Question</p>', unsafe_allow_html=True)
    
    question = st.text_area(
        "Question Input",
        placeholder="What spiritual truth would you like to explore? (e.g., 'What did Jesus actually teach about the Kingdom of God?')",
        height=100,
        key="question_input",
        label_visibility="collapsed"
    )
    
    # Modern tabs for comparison modes
    tab1, tab2, tab3 = st.tabs(["🔄 Original vs Modern", "🌍 Cross-Traditions", "📈 Timeline Evolution"])
    
    with tab1:
        st.markdown('<p class="modern-text">Compare original ancient teachings with modern interpretations</p>', unsafe_allow_html=True)
        comparison_mode = "modern_vs_original"
        selected_traditions = st.multiselect(
            "Select religious traditions to analyze:",
            available_traditions,
            default=["Christianity"] if "Christianity" in available_traditions else []
        )
        time_periods = []
    
    with tab2:
        st.markdown('<p class="modern-text">Compare how different traditions approach the same spiritual concepts</p>', unsafe_allow_html=True)
        comparison_mode = "across_traditions"
        selected_traditions = st.multiselect(
            "Select traditions to compare:",
            available_traditions,
            default=["Christianity", "Buddhism"] if all(t in available_traditions for t in ["Christianity", "Buddhism"]) else available_traditions[:2]
        )
        time_periods = []
    
    with tab3:
        st.markdown('<p class="modern-text">Track how teachings evolved across historical periods</p>', unsafe_allow_html=True)
        comparison_mode = "across_time_periods"
        selected_traditions = st.multiselect(
            "Select traditions for timeline analysis:",
            available_traditions,
            default=["Christianity"] if "Christianity" in available_traditions else []
        )
        time_periods = st.multiselect(
            "Select time periods to analyze:",
            available_time_periods,
            default=available_time_periods[:2] if len(available_time_periods) >= 2 else available_time_periods
        )
    
    # Modern submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔮 Unveil Truth", key="submit_button"):
            if question and selected_traditions:
                st.session_state.is_loading = True
                st.rerun()
            else:
                st.error("Please enter a question and select at least one tradition.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Loading indicator
    if st.session_state.is_loading:
        st.markdown("""
        <div class="status-indicator status-loading">
            <span>AI is analyzing ancient texts</span>
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Perform the query
        result = asyncio.run(query_spiritual_truth(
            question, selected_traditions, comparison_mode, time_periods
        ))
        
        st.session_state.query_results = result
        st.session_state.is_loading = False
        st.rerun()
    
    # Display results
    if st.session_state.query_results:
        result = st.session_state.query_results
        
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.markdown("""
            <div class="status-indicator status-success">
                <span>✨ Truth Analysis Complete</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Modern results display
            st.markdown('<div class="ai-response">', unsafe_allow_html=True)
            
            # Handle different comparison modes
            if comparison_mode == "modern_vs_original":
                if result.get("original_teachings"):
                    st.markdown("### 📜 Original Teachings")
                    st.markdown(f'<div class="modern-text">{result["original_teachings"]}</div>', unsafe_allow_html=True)
                
                if result.get("modern_interpretations"):
                    st.markdown("### 🏛️ Modern Interpretations")
                    st.markdown(f'<div class="modern-text">{result["modern_interpretations"]}</div>', unsafe_allow_html=True)
                
                if result.get("comparison"):
                    st.markdown("### 🔍 Truth Analysis")
                    st.markdown(f'<div class="modern-text">{result["comparison"]}</div>', unsafe_allow_html=True)
                
                if result.get("key_differences"):
                    st.markdown("### ⚡ Key Manipulations Exposed")
                    for diff in result["key_differences"]:
                        st.markdown(f'<div class="modern-text">• {diff}</div>', unsafe_allow_html=True)
            
            elif comparison_mode == "across_traditions":
                if result.get("cross_tradition_analysis"):
                    st.markdown("### 🌍 Cross-Tradition Analysis")
                    st.markdown(f'<div class="modern-text">{result["cross_tradition_analysis"]}</div>', unsafe_allow_html=True)
                
                if result.get("commonalities"):
                    st.markdown("### 🤝 Universal Truths")
                    for common in result["commonalities"]:
                        st.markdown(f'<div class="modern-text">• {common}</div>', unsafe_allow_html=True)
                
                if result.get("unique_elements"):
                    st.markdown("### 🎯 Unique Teachings")
                    for tradition, elements in result["unique_elements"].items():
                        st.markdown(f"**{tradition}:**")
                        for element in elements:
                            st.markdown(f'<div class="modern-text">• {element}</div>', unsafe_allow_html=True)
            
            elif comparison_mode == "across_time_periods":
                if result.get("evolution_analysis"):
                    st.markdown("### 📈 Evolution Analysis")
                    st.markdown(f'<div class="modern-text">{result["evolution_analysis"]}</div>', unsafe_allow_html=True)
                
                if result.get("timeline_data"):
                    st.markdown("### 📅 Historical Timeline")
                    for period_data in result["timeline_data"]:
                        st.markdown(f"**{period_data.get('period', 'Unknown Period')}:**")
                        st.markdown(f'<div class="modern-text">{period_data.get("summary", "No summary available")}</div>', unsafe_allow_html=True)
            
            # Sources section
            if result.get("sources"):
                st.markdown("### 📚 Source Citations")
                with st.expander("View Source Documentation"):
                    for source in result["sources"]:
                        st.markdown(f"**{source.get('title', 'Unknown Title')}**")
                        st.markdown(f"- Tradition: {source.get('tradition', 'Unknown')}")
                        st.markdown(f"- Period: {source.get('period', 'Unknown')}")
                        st.markdown(f"- Citation: {source.get('citation', 'No citation')}")
                        if source.get('relevance'):
                            st.markdown(f"- Relevance: {source['relevance']}")
                        st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Legal Disclaimer Footer
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1.5rem; margin: 2rem 0; color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
        <div style="color: #f97316; font-weight: 600; margin-bottom: 1rem;">⚠️ Disclaimer</div>
        <p>This is an experimental tool provided for personal, educational, and exploratory use only. All features are 100% free. No financial value, utility, or guarantees are implied or provided.</p>
        
        <div style="margin: 1rem 0; font-size: 0.85rem;">
            <a href="#" style="color: #667eea; text-decoration: none;">View Full Disclaimer</a> | 
            <a href="#" style="color: #667eea; text-decoration: none;">GitHub Legal Notice</a>
        </div>
        
        <p style="margin-bottom: 0.5rem;">This project is experimental and created for entertainment and exploratory purposes only. It does not offer financial utility, investment promises, or future returns of any kind.</p>
        
        <p style="margin-bottom: 0.5rem;">The associated token (if launched) has no inherent value and is not intended for speculation, profit, or investment. It is not a security, utility token, or financial instrument.</p>
        
        <p style="margin-bottom: 0;">By interacting with this app or token, you acknowledge that it is for fun, curiosity, and community exploration — not for financial gain.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #64748b;">
        <p>Divine Mirror AI - Revealing truth through ancient wisdom</p>
        <p style="font-size: 0.9rem;">The Kingdom of God is within you</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()