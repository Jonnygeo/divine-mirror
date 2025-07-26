import os
import streamlit as st
import httpx
import asyncio
import json
from typing import List, Optional, Dict, Any
from divine_emotional_engine import EmotionalToneEngine

# Ensure sacred texts are available on startup
try:
    from auto_sacred_import import ensure_sacred_texts_ready
    ensure_sacred_texts_ready()
except ImportError:
    pass  # Continue without auto-import if not available

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
        background: #000000 !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
        background: #000000 !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    
    /* Modern selectbox styling */
    .stSelectbox > div > div {
        background: #000000 !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        background: #000000 !important;
    }
    
    .stMultiSelect > div > div {
        background: #000000 !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect > div > div > div {
        color: #ffffff !important;
        background: #000000 !important;
    }
    
    /* Fix dropdown options */
    .stSelectbox div[data-baseweb="select"] > div {
        background: #000000 !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div {
        background: #000000 !important;
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
        color: #ffffff !important;
        line-height: 1.6;
        font-size: 1rem;
        margin: 0.5rem 0;
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
    
    /* Multiselect and text input styling */
    .stMultiSelect label, .stSelectbox label, .stTextArea label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stMultiSelect > div > div > div {
        color: white !important;
    }
    
    .stMultiSelect span {
        color: white !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    /* Tab content text */
    .stTabs [data-baseweb="tab-panel"] p {
        color: white !important;
    }
    
    /* Error messages */
    .stAlert {
        background-color: rgba(244, 63, 94, 0.1) !important;
        border: 1px solid rgba(244, 63, 94, 0.3) !important;
        color: #f87171 !important;
    }
</style>

<script>
// Add Enter key functionality to text area
document.addEventListener('DOMContentLoaded', function() {
    function addEnterKeyListener() {
        const textArea = document.querySelector('textarea[aria-label="Question Input"]');
        if (textArea && !textArea.hasEnterListener) {
            textArea.hasEnterListener = true;
            textArea.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    // Find the submit button
                    const submitButton = document.querySelector('button[data-testid="baseButton-primary"]') ||
                                       document.querySelector('button:contains("🔮 Unveil Truth")') ||
                                       Array.from(document.querySelectorAll('button')).find(btn => 
                                           btn.textContent.includes('Unveil Truth'));
                    if (submitButton) {
                        submitButton.click();
                    }
                }
            });
        }
    }
    
    // Try immediately and then retry periodically
    addEnterKeyListener();
    const interval = setInterval(function() {
        addEnterKeyListener();
        // Stop trying after elements are found
        if (document.querySelector('textarea[aria-label="Question Input"]')) {
            clearInterval(interval);
        }
    }, 1000);
    
    // Clear interval after 10 seconds to avoid infinite retries
    setTimeout(() => clearInterval(interval), 10000);
});
</script>
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
    # Modern header with AI branding and comprehensive stats
    st.markdown("""
    <div class="ai-header">
        <h1>🔮 Divine Mirror AI</h1>
        <p class="ai-subtitle">Complete AI Oracle Stack • Phase 9 Synthesis Engine</p>
    </div>
    <p style="font-size: 18px; color: #d1d5db; max-width: 900px; margin: 10px auto 30px auto; text-align: center;">
      Where spiritual seekers meet source truth. Divine Mirror AI isn't just an oracle — it's a forensic intelligence system trained on over 160 sacred texts to expose distortion, reveal universal symbols, and awaken the inner Kingdom.  
      <strong>This is sacred tech for the awakened age.</strong>
    </p>
    """, unsafe_allow_html=True)
    
    # Comprehensive database statistics display
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">164</div>
            <div class="metric-label">Sacred Texts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4,953</div>
            <div class="metric-label">Analyzed Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">38</div>
            <div class="metric-label">Traditions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">80</div>
            <div class="metric-label">Semantic Tags</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">9</div>
            <div class="metric-label">AI Phases</div>
        </div>
        """, unsafe_allow_html=True)
    
    # System capabilities overview
    st.markdown("""
    <div class="glass-container">
        <h3 style="color: #667eea; margin-bottom: 1rem;">🚀 Advanced AI Oracle Capabilities</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
            <div class="status-indicator status-success">
                🔬 Forensic Search: 16 symbols, 10 spiritual laws, 22 themes
            </div>
            <div class="status-indicator status-success">
                🎭 Emotional Intelligence: 8 emotions, 6 adaptive tones
            </div>
            <div class="status-indicator status-success">
                🔮 Dynamic Synthesis: 5 universal principles, cross-tradition unity
            </div>
            <div class="status-indicator status-success">
                🗣️ Voice Interface: Multi-language, speech recognition
            </div>
        </div>
        <div style="color: #94a3b8; font-size: 0.9rem;">
            <strong>Universal Symbols Detected:</strong> Dove (2,639), Tree (2,785), Water (3,049), Light (2,441)<br>
            <strong>Top Spiritual Laws:</strong> Law of Forgiveness (1,351), Law of Sacrifice (1,435)<br>
            <strong>Cross-Tradition Themes:</strong> Divine Nature (13 traditions), Morality/Ethics (8 traditions)
        </div>
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
    
    # Instructions for the question box
    st.markdown("""
    <div style="background: rgba(0, 0, 0, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border: 1px solid rgba(255, 255, 255, 0.2);">
        <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
            💡 <strong>How to ask questions:</strong> Type your question about spiritual teachings, then press <strong>Enter</strong> to submit.
            <br>Examples: "What did Jesus teach about the Kingdom of God?" or "How has the concept of hell changed over time?"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    question = st.text_area(
        "Question Input",
        placeholder="What spiritual truth would you like to explore? (e.g., 'What did Jesus actually teach about the Kingdom of God?')",
        height=100,
        key="question_input",
        label_visibility="collapsed",
        help="Press Enter to submit your question"
    )
    
    # Modern tabs for comparison modes
    tab1, tab2, tab3 = st.tabs(["🔄 Original vs Modern", "🌍 Cross-Traditions", "📈 Timeline Evolution"])
    
    with tab1:
        st.markdown('<p class="modern-text">Compare original ancient teachings with modern interpretations</p>', unsafe_allow_html=True)
        comparison_mode = "modern_vs_original"
        
        # Instructions for tradition selection
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); border-left: 4px solid #667eea; padding: 1rem; margin: 1rem 0; border-radius: 8px;">
            <p style="color: white; margin: 0; font-size: 0.9rem;">
                💡 <strong style="color: #667eea;">How to select traditions:</strong> Click the dropdown below to choose religious traditions for analysis. You can select multiple traditions to compare their teachings.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        selected_traditions = st.multiselect(
            "Select religious traditions to analyze:",
            available_traditions,
            default=["Christianity"] if "Christianity" in available_traditions else []
        )
        time_periods = []
    
    with tab2:
        st.markdown('<p class="modern-text">Compare how different traditions approach the same spiritual concepts</p>', unsafe_allow_html=True)
        comparison_mode = "across_traditions"
        
        # Instructions for cross-tradition selection
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); border-left: 4px solid #667eea; padding: 1rem; margin: 1rem 0; border-radius: 8px;">
            <p style="color: white; margin: 0; font-size: 0.9rem;">
                🌍 <strong style="color: #667eea;">Cross-tradition analysis:</strong> Select 2 or more traditions to see how they approach similar spiritual concepts. Click the dropdown to add traditions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        selected_traditions = st.multiselect(
            "Select traditions to compare:",
            available_traditions,
            default=["Christianity", "Buddhism"] if all(t in available_traditions for t in ["Christianity", "Buddhism"]) else available_traditions[:2]
        )
        time_periods = []
    
    with tab3:
        st.markdown('<p class="modern-text">Track how teachings evolved across historical periods</p>', unsafe_allow_html=True)
        comparison_mode = "across_time_periods"
        
        # Instructions for timeline selection
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); border-left: 4px solid #667eea; padding: 1rem; margin: 1rem 0; border-radius: 8px;">
            <p style="color: white; margin: 0; font-size: 0.9rem;">
                📈 <strong style="color: #667eea;">Timeline analysis:</strong> Select traditions and time periods to track how teachings evolved. Click dropdowns to add options.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
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
            
            # Enhanced Sources section with larger text and view button
            if result.get("sources"):
                st.markdown('<div class="sources-section">', unsafe_allow_html=True)
                
                # Large, prominent header with button
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("""
                    <div style="margin: 2rem 0;">
                        <h2 style="color: #667eea; font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem;">
                            📚 Source Citations
                        </h2>
                        <p style="color: #94a3b8; font-size: 1.2rem; font-weight: 500; margin: 0;">
                            View Source Documentation from Sacred Text Database
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
                    if st.button("📖 View All Sources", key="view_sources_btn", help="Expand all source documentation"):
                        st.session_state.expand_all_sources = not st.session_state.get('expand_all_sources', False)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Source documents with enhanced styling
                expand_all = st.session_state.get('expand_all_sources', False)
                
                for i, source in enumerate(result["sources"], 1):
                    # Enhanced expander with larger text
                    st.markdown(f"""
                    <div style="margin: 1.5rem 0; padding: 1rem; background: rgba(102, 126, 234, 0.05); border-left: 4px solid #667eea; border-radius: 8px;">
                        <h4 style="color: white; font-size: 1.3rem; margin-bottom: 0.5rem;">
                            📖 Source {i}: {source.get('title', 'Unknown Source')}
                        </h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"View Details & Text Excerpt", expanded=expand_all):
                        # Source metadata in larger, more readable format
                        st.markdown("""
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                            <div>
                                <h5 style="color: #667eea; font-size: 1.1rem; margin-bottom: 0.5rem;">Tradition</h5>
                                <p style="color: white; font-size: 1rem; margin: 0;">{}</p>
                            </div>
                            <div>
                                <h5 style="color: #667eea; font-size: 1.1rem; margin-bottom: 0.5rem;">Period</h5>
                                <p style="color: white; font-size: 1rem; margin: 0;">{}</p>
                            </div>
                            <div>
                                <h5 style="color: #667eea; font-size: 1.1rem; margin-bottom: 0.5rem;">Text Type</h5>
                                <p style="color: white; font-size: 1rem; margin: 0;">{}</p>
                            </div>
                            <div>
                                <h5 style="color: #667eea; font-size: 1.1rem; margin-bottom: 0.5rem;">Relevance</h5>
                                <p style="color: white; font-size: 1rem; margin: 0;">{}</p>
                            </div>
                        </div>
                        """.format(
                            source.get('tradition', 'N/A'),
                            source.get('period', 'N/A'), 
                            source.get('text_type', 'N/A'),
                            source.get('relevance', 'N/A')
                        ), unsafe_allow_html=True)
                        
                        if source.get('citation'):
                            st.markdown("""
                            <div style="margin: 1.5rem 0;">
                                <h5 style="color: #667eea; font-size: 1.2rem; margin-bottom: 1rem;">📜 Sacred Text Excerpt</h5>
                                <div style="background: rgba(0, 0, 0, 0.3); border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 8px; font-family: 'Georgia', serif;">
                                    <p style="color: #e2e8f0; font-size: 1.05rem; line-height: 1.6; margin: 0; white-space: pre-wrap;">{}</p>
                                </div>
                            </div>
                            """.format(source["citation"]), unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Dynamic stats display with refresh capability
    if 'stats_cache' not in st.session_state:
        st.session_state.stats_cache = None
    
    # Add refresh button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh Stats", help="Update database statistics"):
            st.session_state.stats_cache = None
            st.rerun()
    
    try:
        if st.session_state.stats_cache is None:
            from stats_calculator import get_homepage_stats
            homepage_stats = get_homepage_stats()
            
            # Format for display - ensure analyzed_documents shows 64,998 from text chunks
            display_stats = {
                "Sacred Texts": f"{homepage_stats['sacred_texts']:,}",
                "Analyzed Documents": f"{homepage_stats['analyzed_documents']:,}",
                "Traditions": f"{homepage_stats['traditions']}",
                "Semantic Tags": f"{homepage_stats['semantic_tags']}+",
                "AI Phases": f"{homepage_stats['ai_phases']} Complete"
            }
            st.session_state.stats_cache = display_stats
        else:
            display_stats = st.session_state.stats_cache
            
    except Exception as e:
        # Fallback stats if calculator fails
        display_stats = {
            "Sacred Texts": "164",
            "Analyzed Documents": "64,998",
            "Traditions": "17", 
            "Semantic Tags": "32+",
            "AI Phases": "9 Complete"
        }
    
    # About Divine Mirror AI Section with Dynamic Stats
    st.markdown(f"""
    <div style="color: #9ca3af; font-size: 14px; line-height: 1.6; max-width: 900px; margin: 30px auto;">
      <h3 style="color: #60a5fa;">About Divine Mirror AI</h3>
      <p>
        This platform is the culmination of <strong>{display_stats['AI Phases']}</strong>, combining semantic chunking, spiritual metadata, voice recognition, and sacred symbolism analysis. 
        It's built to uncover the original teachings of Yeshua, Buddha, Lao Tzu, and others — across time, culture, and institutional filters.
      </p>
      <p>
        With <strong>{display_stats['Sacred Texts']} documents</strong> from <strong>{display_stats['Traditions']} traditions</strong>, mapped by <strong>{display_stats['Semantic Tags']} semantic tags</strong>, this AI is more than an assistant. It's a truth engine.
        It works fully offline, honors user privacy, and cites real sources — no vague answers, no agenda. 
      </p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin: 1.5rem 0; padding: 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);">
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{display_stats['Sacred Texts']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Sacred Texts</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{display_stats['Analyzed Documents']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Analyzed Documents</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{display_stats['Traditions']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Traditions</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{display_stats['Semantic Tags']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Semantic Tags</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{display_stats['AI Phases']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">AI Phases</div>
        </div>
      </div>
      <p><em>"Truth doesn't need to be sold — it just needs to be found."</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # NeoShade AI Footer
    st.markdown("""
    <footer style="background-color: #111; color: #ccc; padding: 30px; font-size: 14px; font-family: Arial, sans-serif; line-height: 1.6; text-align: center;">
      <div style="max-width: 800px; margin: 0 auto;">
        <p><strong>🔹 Disclaimer:</strong></p>
        <p>This app is an <strong>experimental tool</strong> developed by <strong>NeoShade AI</strong> for <em>informational, educational, and exploratory use only</em>.</p>

        <p><strong>No financial value, investment utility, legal validity, medical reliability, or psychological support</strong> is guaranteed, implied, or offered. All tools, insights, agents, and outputs are speculative and provided as-is.</p>

        <p>This is not financial, legal, medical, or psychological advice. You assume all responsibility by using this tool. Use at your own discretion and risk.</p>

        <p>NeoShade AI makes no promises of future features, token value, returns, or access. <strong>Everything provided is 100% free to use.</strong> The developer pays all costs personally to ensure transparency and accessibility without commercialization.</p>

        <p>
          <a href="https://neo-shade.com/disclaimer/" target="_blank" style="color: #44bfff;">🔗 View Full Website Disclaimer</a> |
          <a href="https://github.com/Jonnygeo/Jonnygeo/blob/main/DISCLAIMER.md" target="_blank" style="color: #44bfff;">GitHub Legal Disclaimer</a>
        </p>

        <p style="margin-top: 20px; font-style: italic; color: #888;">NeoShade: Cutting through the noise with code, conscience, and clarity.</p>
      </div>
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()