#!/usr/bin/env python3
"""
Divine Mirror AI - Voice-Enhanced Streamlit Application
Main application with integrated voice interface capabilities
"""

import streamlit as st
import json
import requests
from pathlib import Path
from divine_voice_interface import VoiceInterface
from divine_advanced_search import AdvancedSearchEngine
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Divine Mirror AI - Voice Oracle",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for voice interface
st.markdown("""
<style>
    .voice-container {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
    }
    
    .voice-button {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 1.2em;
        color: white;
        cursor: pointer;
        margin: 10px;
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ffd700;
    }
    
    .tradition-tag {
        background: #ffd700;
        color: #1e3c72;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'voice_interface' not in st.session_state:
    st.session_state.voice_interface = VoiceInterface()

if 'search_engine' not in st.session_state:
    st.session_state.search_engine = AdvancedSearchEngine()

# Main header
st.title("🎤 Divine Mirror AI - Voice Oracle")
st.markdown("**Speak to the Sacred Texts Across 17 Religious Traditions**")

# Sidebar navigation
with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio("Choose Interface:", [
        "🎤 Voice Search",
        "🔍 Advanced Search", 
        "📊 Database Statistics",
        "🌍 Cross-Tradition Analysis"
    ])
    
    st.markdown("---")
    st.header("📚 Database Info")
    if st.session_state.voice_interface.documents:
        st.metric("Total Documents", len(st.session_state.voice_interface.documents))
        st.metric("Search Tags", len(st.session_state.voice_interface.tag_statistics))
        
        # Top traditions
        st.subheader("Top Traditions")
        tradition_tags = {k: v for k, v in st.session_state.voice_interface.tag_statistics.items() 
                         if k.startswith('tradition_')}
        for tag, count in sorted(tradition_tags.items(), key=lambda x: x[1], reverse=True)[:5]:
            tradition = tag.replace('tradition_', '').title()
            st.write(f"**{tradition}**: {count}")

# Voice Search Page
if page == "🎤 Voice Search":
    st.header("Voice-Driven Sacred Text Search")
    
    # Voice interface container
    with st.container():
        st.markdown('<div class="voice-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.subheader("🎤 Voice Input")
            
            # Language selection
            language = st.selectbox(
                "Select Language:",
                ["English", "Hebrew", "Greek", "Arabic", "Sanskrit"],
                key="voice_language"
            )
            
            # Voice button placeholder
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <button class="voice-button" onclick="startVoiceRecognition()">
                    🎤 Click to Speak
                </button>
                <p style="margin-top: 10px; opacity: 0.8;">
                    Ask questions like: "What did Yeshua teach about the kingdom within?"
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='text-align: center; padding: 50px 0;'>OR</div>", unsafe_allow_html=True)
        
        with col3:
            st.subheader("⌨️ Text Input")
            
            text_query = st.text_input(
                "Type your question:",
                placeholder="What did Buddha teach about suffering?",
                key="text_query"
            )
            
            if st.button("🔍 Search Texts", type="primary"):
                if text_query:
                    with st.spinner("Searching sacred texts..."):
                        response = st.session_state.voice_interface.process_voice_command(text_query)
                        st.session_state.last_response = response
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display results
    if 'last_response' in st.session_state and st.session_state.last_response:
        response = st.session_state.last_response
        
        st.header("🎯 Search Results")
        
        # Response summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Results Found", response['results_count'])
        with col2:
            st.metric("Language", response['language_name'])
        with col3:
            if st.button("🗣️ Speak Response"):
                st.info("Text-to-speech would play here in full implementation")
        
        # Detailed results
        if response['detailed_results']:
            for i, result in enumerate(response['detailed_results'], 1):
                with st.expander(f"📖 Result {i}: {result['tradition']} - {result['title']}"):
                    st.markdown(f"""
                    <div class="result-card">
                        <span class="tradition-tag">{result['tradition']}</span>
                        <strong>Relevance Score:</strong> {result['score']}<br><br>
                        <div style="line-height: 1.6;">{result['text']}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Advanced Search Page
elif page == "🔍 Advanced Search":
    st.header("Advanced Semantic Search")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("Search Query:", placeholder="divine nature, love, kingdom within")
        
        # Filters
        st.subheader("🎛️ Filters")
        
        col_a, col_b = st.columns(2)
        with col_a:
            tradition_filter = st.selectbox(
                "Tradition:",
                ["All"] + sorted([tag.replace('tradition_', '').title() 
                                for tag in st.session_state.voice_interface.tag_statistics.keys() 
                                if tag.startswith('tradition_')])
            )
        
        with col_b:
            period_filter = st.selectbox("Period:", ["All", "Ancient", "Medieval", "Modern"])
    
    with col2:
        st.subheader("🏷️ Available Tags")
        concept_tags = [tag for tag in st.session_state.voice_interface.tag_statistics.keys() 
                       if not tag.startswith(('tradition_', 'period_', 'type_'))][:15]
        
        selected_tags = st.multiselect("Concept Tags:", concept_tags)
    
    if st.button("🔍 Advanced Search", type="primary"):
        if search_query or selected_tags:
            with st.spinner("Performing advanced search..."):
                # Build filters
                filters = {}
                if tradition_filter != "All":
                    filters['tradition'] = tradition_filter
                if period_filter != "All":
                    filters['period'] = period_filter
                
                # Perform search
                results = st.session_state.search_engine.advanced_search(
                    search_query, 
                    filters=filters if filters else None,
                    tag_filters=selected_tags if selected_tags else None,
                    max_results=10
                )
                
                st.header(f"🎯 Found {len(results)} Results")
                
                for i, result in enumerate(results, 1):
                    metadata = result['metadata']
                    with st.expander(f"📖 {i}. [{metadata.get('tradition', 'Unknown')}] {metadata.get('title', 'Unknown')}"):
                        st.write(f"**Period:** {metadata.get('period', 'Unknown')}")
                        st.write(f"**Type:** {metadata.get('type', 'Unknown')}")
                        st.write(f"**Tags:** {', '.join(metadata.get('tags', [])[:8])}")
                        st.write(f"**Relevance Score:** {result['score']}")
                        st.markdown("---")
                        st.write(result['document'])

# Database Statistics Page
elif page == "📊 Database Statistics":
    st.header("Database Statistics & Analysis")
    
    if st.session_state.voice_interface.documents:
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", len(st.session_state.voice_interface.documents))
        
        with col2:
            st.metric("Semantic Tags", len(st.session_state.voice_interface.tag_statistics))
        
        with col3:
            tradition_count = len([tag for tag in st.session_state.voice_interface.tag_statistics.keys() 
                                 if tag.startswith('tradition_')])
            st.metric("Religious Traditions", tradition_count)
        
        with col4:
            concept_count = len([tag for tag in st.session_state.voice_interface.tag_statistics.keys() 
                               if not tag.startswith(('tradition_', 'period_', 'type_'))])
            st.metric("Concept Categories", concept_count)
        
        # Top concepts chart
        st.subheader("🔝 Top Spiritual Concepts")
        
        concept_data = {tag: count for tag, count in st.session_state.voice_interface.tag_statistics.items() 
                       if not tag.startswith(('tradition_', 'period_', 'type_'))}
        
        top_concepts = sorted(concept_data.items(), key=lambda x: x[1], reverse=True)[:15]
        
        for concept, count in top_concepts:
            st.write(f"**{concept.replace('_', ' ').title()}**: {count} documents")
        
        # Tradition breakdown
        st.subheader("🌍 Tradition Distribution")
        
        tradition_data = {tag.replace('tradition_', '').title(): count 
                         for tag, count in st.session_state.voice_interface.tag_statistics.items() 
                         if tag.startswith('tradition_')}
        
        for tradition, count in sorted(tradition_data.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(st.session_state.voice_interface.documents)) * 100
            st.write(f"**{tradition}**: {count} documents ({percentage:.1f}%)")

# Cross-Tradition Analysis Page
elif page == "🌍 Cross-Tradition Analysis":
    st.header("Cross-Tradition Comparative Analysis")
    
    st.write("Compare how different religious traditions approach the same concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Compare Traditions")
        
        traditions = sorted([tag.replace('tradition_', '').title() 
                           for tag in st.session_state.voice_interface.tag_statistics.keys() 
                           if tag.startswith('tradition_')])
        
        tradition_a = st.selectbox("First Tradition:", traditions, key="tradition_a")
        tradition_b = st.selectbox("Second Tradition:", traditions, key="tradition_b")
        comparison_topic = st.text_input("Topic to Compare:", placeholder="salvation, love, divine nature")
        
        if st.button("🔄 Compare Traditions"):
            if tradition_a and tradition_b and comparison_topic:
                st.write(f"Comparing **{tradition_a}** vs **{tradition_b}** on topic: **{comparison_topic}**")
                
                # This would integrate with the cross-comparison engine
                st.info("Cross-tradition comparison results would appear here")
    
    with col2:
        st.subheader("📊 Universal Themes")
        
        # Show top cross-tradition concepts
        universal_concepts = [
            ("morality_ethics", "8 traditions, 2,777 documents"),
            ("divine_nature", "13 traditions, 2,438 documents"),
            ("soul_spirit", "8 traditions, 2,077 documents"),
            ("love_compassion", "5 traditions, 912 documents"),
            ("peace_harmony", "4 traditions, 654 documents")
        ]
        
        for concept, description in universal_concepts:
            st.write(f"**{concept.replace('_', ' ').title()}**: {description}")

# Voice interface JavaScript integration
voice_js = """
<script>
function startVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            console.log('Voice recognition started');
            alert('Listening... Please speak your question');
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            console.log('Transcript:', transcript);
            
            // Update the text input field
            const textInput = document.querySelector('input[data-testid="stTextInput"]');
            if (textInput) {
                textInput.value = transcript;
                textInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            
            alert('You said: "' + transcript + '"');
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            alert('Speech recognition error: ' + event.error);
        };
        
        recognition.start();
    } else {
        alert('Speech recognition not supported in this browser');
    }
}
</script>
"""

st.markdown(voice_js, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; opacity: 0.7;'>
    <p>🎤 Divine Mirror AI - Voice-Driven Sacred Text Oracle<br>
    164 Sacred Texts • 17 Religious Traditions • 4,953 Semantic Chunks</p>
</div>
""", unsafe_allow_html=True)