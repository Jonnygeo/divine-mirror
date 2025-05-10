import os
import streamlit as st
import httpx
from frontend.components import (
    render_header,
    render_question_form,
    render_results_view,
    render_timeline_view,
    render_source_citations
)

# Configure page
st.set_page_config(
    page_title="Divine Mirror AI - Spiritual Truth Comparison",
    page_icon="✨",
    layout="wide",
)

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

# Functions to communicate with the backend
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
                timeout=120.0  # Extended timeout for complex queries
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
            return None

async def get_available_traditions():
    """Retrieve available religious traditions from the backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/traditions")
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error retrieving traditions: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
            return []

async def get_time_periods():
    """Retrieve available time periods from the backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/time_periods")
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error retrieving time periods: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
            return []

# Main function to run the application
def main():
    # Render application header
    render_header()
    
    # Sidebar for filters and options
    st.sidebar.title("Filters & Options")
    
    # Fetch available traditions (non-blocking)
    @st.cache_data(ttl=3600)
    def get_traditions():
        import asyncio
        return asyncio.run(get_available_traditions())
    
    # Fetch available time periods (non-blocking)
    @st.cache_data(ttl=3600)
    def fetch_time_periods():
        import asyncio
        return asyncio.run(get_time_periods())
    
    # Get available traditions and time periods
    available_traditions = get_traditions()
    available_time_periods = fetch_time_periods()
    
    # Filter selections
    st.session_state.selected_traditions = st.sidebar.multiselect(
        "Select Religious Traditions",
        options=available_traditions,
        default=[] if not st.session_state.selected_traditions else st.session_state.selected_traditions
    )
    
    st.session_state.comparison_mode = st.sidebar.selectbox(
        "Comparison Mode",
        options=["modern_vs_original", "across_time_periods", "across_traditions"],
        index=0 if st.session_state.comparison_mode == "modern_vs_original" else 
              1 if st.session_state.comparison_mode == "across_time_periods" else 2
    )
    
    # Only show time periods selection if comparing across time
    if st.session_state.comparison_mode == "across_time_periods":
        st.session_state.time_periods = st.sidebar.multiselect(
            "Select Time Periods to Compare",
            options=available_time_periods,
            default=[] if not st.session_state.time_periods else st.session_state.time_periods
        )
    
    # Disclaimer and about section
    with st.sidebar.expander("About Divine Mirror AI"):
        st.write("""
        Divine Mirror AI helps you explore spiritual truths across different traditions 
        and time periods. The system compares original religious teachings with modern 
        interpretations to reveal how they've evolved throughout history.
        
        Our goal is to provide an unbiased, objective view of spiritual teachings 
        based on authentic source texts, not to promote any particular belief system.
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Ask about spiritual truths")
        question, submit_clicked = render_question_form()
        
        if submit_clicked:
            if not question:
                st.warning("Please enter a question.")
            elif not st.session_state.selected_traditions:
                st.warning("Please select at least one religious tradition.")
            elif st.session_state.comparison_mode == "across_time_periods" and not st.session_state.time_periods:
                st.warning("Please select at least one time period for comparison.")
            else:
                with st.spinner("Seeking divine wisdom..."):
                    import asyncio
                    results = asyncio.run(query_spiritual_truth(
                        question,
                        st.session_state.selected_traditions,
                        st.session_state.comparison_mode,
                        st.session_state.time_periods
                    ))
                    if results:
                        st.session_state.query_results = results
                        st.session_state.sources = results.get("sources", [])
    
    with col2:
        if st.session_state.query_results:
            # Render different views based on comparison mode
            if st.session_state.comparison_mode == "modern_vs_original":
                render_results_view(st.session_state.query_results)
            elif st.session_state.comparison_mode == "across_time_periods":
                render_timeline_view(st.session_state.query_results)
            else:  # across_traditions
                render_results_view(st.session_state.query_results, mode="traditions")
            
            # Show sources
            if st.session_state.sources:
                with st.expander("Source Citations"):
                    render_source_citations(st.session_state.sources)
        else:
            st.info("""
            ### Welcome to Divine Mirror AI
            
            Ask a question about spiritual teachings across different traditions 
            and discover how these concepts have evolved over time.
            
            **Example questions:**
            - What do different traditions teach about the soul's journey after death?
            - How has the concept of divine love changed from ancient to modern Christianity?
            - What are the original teachings about meditation in Buddhist texts?
            - Compare the concept of salvation across different religious traditions.
            """)

if __name__ == "__main__":
    main()
