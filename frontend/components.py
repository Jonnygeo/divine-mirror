import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

def render_header():
    """Renders the application header with title and description"""
    st.title("✨ Divine Mirror AI")
    st.markdown("""
    ### Uncover Spiritual Truths Across Time & Tradition
    
    Compare original religious teachings with modern interpretations and 
    discover how spiritual concepts have evolved throughout history.
    """)
    st.divider()

def render_question_form():
    """Renders the question input form and returns the question and submit status"""
    with st.form(key="question_form"):
        question = st.text_area(
            "Enter your spiritual or religious question:",
            height=100,
            placeholder="E.g., What do different traditions teach about the soul's journey after death?"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.form_submit_button("Search")
        with col2:
            st.markdown("*Ask any question about spiritual teachings or concepts*")
    
    return question, submit_button

def render_results_view(results, mode="modern_original"):
    """Renders the comparison view between modern and original teachings"""
    if not results:
        st.warning("No results found. Please try a different question or select different traditions.")
        return
    
    st.subheader("Results")
    
    if mode == "modern_original":
        tabs = st.tabs(["Original Teachings", "Modern Interpretations", "Comparison"])
        
        with tabs[0]:
            st.markdown("### Original Teachings")
            st.markdown(results.get("original_teachings", "No original teachings data found."))
        
        with tabs[1]:
            st.markdown("### Modern Interpretations")
            st.markdown(results.get("modern_interpretations", "No modern interpretations found."))
        
        with tabs[2]:
            st.markdown("### How Teachings Have Changed")
            st.markdown(results.get("comparison", "No comparison data found."))
            
            # Show key differences as bullet points if available
            if "key_differences" in results and results["key_differences"]:
                st.markdown("#### Key Differences")
                for diff in results["key_differences"]:
                    st.markdown(f"- {diff}")
    
    elif mode == "traditions":
        # Get the list of traditions in the results
        traditions = list(results.get("traditions_comparison", {}).keys())
        
        if not traditions:
            st.warning("No tradition-specific data found.")
            return
        
        # Create tabs for each tradition and a comparison tab
        tabs = st.tabs(traditions + ["Comparison"])
        
        # Fill in tradition-specific tabs
        for i, tradition in enumerate(traditions):
            with tabs[i]:
                st.markdown(f"### {tradition}")
                tradition_data = results.get("traditions_comparison", {}).get(tradition, "")
                st.markdown(tradition_data)
        
        # Comparison tab
        with tabs[-1]:
            st.markdown("### Comparison Across Traditions")
            st.markdown(results.get("cross_tradition_analysis", "No cross-tradition analysis available."))
            
            # Show commonalities and differences as bullet points if available
            if "commonalities" in results and results["commonalities"]:
                st.markdown("#### Common Elements")
                for common in results["commonalities"]:
                    st.markdown(f"- {common}")
            
            if "unique_elements" in results and results["unique_elements"]:
                st.markdown("#### Unique Elements")
                for tradition, elements in results["unique_elements"].items():
                    st.markdown(f"**{tradition}**")
                    for element in elements:
                        st.markdown(f"- {element}")

def render_timeline_view(results):
    """Renders a timeline view showing how concepts evolved across different time periods"""
    if not results or "timeline_data" not in results:
        st.warning("No timeline data available for this query.")
        return
    
    st.subheader("Timeline of Teachings")
    
    timeline_data = results.get("timeline_data", [])
    if not timeline_data:
        st.warning("No timeline data points found.")
        return
    
    # Create time period tabs
    time_periods = [item["period"] for item in timeline_data]
    tabs = st.tabs(time_periods + ["Evolution Overview"])
    
    # Fill in period-specific tabs
    for i, period in enumerate(time_periods):
        with tabs[i]:
            period_data = timeline_data[i]
            st.markdown(f"### {period}")
            st.markdown(period_data.get("description", "No description available."))
            
            # Display key texts from this period
            if "key_texts" in period_data and period_data["key_texts"]:
                st.markdown("#### Key Texts")
                for text in period_data["key_texts"]:
                    st.markdown(f"- {text}")
    
    # Evolution overview tab
    with tabs[-1]:
        st.markdown("### How This Teaching Evolved")
        st.markdown(results.get("evolution_analysis", "No evolution analysis available."))
        
        # Create a visual timeline if data points are available
        if timeline_data:
            # Prepare data for chart
            chart_data = []
            for item in timeline_data:
                period = item["period"]
                # Extract year from period for chronological ordering
                # Assuming format like "Ancient (3000-1000 BCE)" or "Medieval (500-1500 CE)"
                year = 0
                try:
                    if "BCE" in period or "BC" in period:
                        # For BCE dates, use negative values
                        year_str = period.split("(")[1].split(")")[0].split("-")[0].strip()
                        year = -int(''.join(filter(str.isdigit, year_str)))
                    else:
                        # For CE dates
                        year_str = period.split("(")[1].split(")")[0].split("-")[0].strip()
                        year = int(''.join(filter(str.isdigit, year_str)))
                except:
                    # If parsing fails, use index as year to maintain order
                    year = timeline_data.index(item)
                
                chart_data.append({
                    "Period": period,
                    "Year": year,
                    "Key Concepts": item.get("key_concepts", ""),
                    "Description": item.get("description", "")[:100] + "..." # Truncate for display
                })
            
            # Create a DataFrame for the chart
            if chart_data:
                df = pd.DataFrame(chart_data)
                
                # Sort by year to ensure chronological order
                df = df.sort_values("Year")
                
                # Create a simple timeline visualization
                timeline_chart = alt.Chart(df).mark_circle(size=100).encode(
                    x=alt.X('Year:Q', title='Timeline (approximate)'),
                    y=alt.Y('Period:N', title=None, sort=None),
                    tooltip=['Period', 'Key Concepts', 'Description']
                ).properties(
                    width=600,
                    height=300,
                    title='Timeline of Teaching Evolution'
                )
                
                # Display the chart
                st.altair_chart(timeline_chart, use_container_width=True)

def render_source_citations(sources):
    """Renders the source citations section"""
    if not sources:
        st.info("No sources cited for this query.")
        return
    
    st.markdown("### Sources")
    
    for i, source in enumerate(sources):
        st.markdown(f"**{i+1}. {source.get('title', 'Unknown Source')}**")
        st.markdown(f"*{source.get('tradition', '')} - {source.get('period', '')}*")
        if "citation" in source:
            st.markdown(f"Citation: {source['citation']}")
        if "relevance" in source:
            st.markdown(f"Relevance: {source['relevance']}")
        st.divider()
