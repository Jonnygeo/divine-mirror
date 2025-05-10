from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SourceCitation(BaseModel):
    """Model for source citations"""
    title: str = Field(..., description="Title of the source text")
    tradition: str = Field(..., description="Religious tradition of the source")
    period: str = Field(..., description="Time period of the source")
    citation: str = Field(..., description="Formatted citation for the source")
    relevance: Optional[str] = Field(None, description="Relevance to the query")
    text_type: Optional[str] = Field(None, description="Type of text (original, commentary, modern)")

class QueryRequest(BaseModel):
    """Model for query requests"""
    question: str = Field(..., description="User's question about spiritual truth")
    traditions: List[str] = Field(..., description="List of religious traditions to query")
    comparison_mode: str = Field(
        "modern_vs_original", 
        description="Type of comparison (modern_vs_original, across_time_periods, across_traditions)"
    )
    time_periods: Optional[List[str]] = Field(
        None, 
        description="List of time periods to compare (required for across_time_periods mode)"
    )

class QueryResponse(BaseModel):
    """Model for query responses"""
    # Fields for modern_vs_original comparison
    original_teachings: Optional[str] = Field(None, description="Summary of original teachings")
    modern_interpretations: Optional[str] = Field(None, description="Summary of modern interpretations")
    comparison: Optional[str] = Field(None, description="Comparison between original and modern")
    key_differences: Optional[List[str]] = Field(None, description="Key differences as bullet points")
    
    # Fields for across_time_periods comparison
    evolution_analysis: Optional[str] = Field(None, description="Analysis of teaching evolution")
    timeline_data: Optional[List[Dict[str, Any]]] = Field(None, description="Timeline data for each period")
    
    # Fields for across_traditions comparison
    traditions_comparison: Optional[Dict[str, str]] = Field(None, description="Comparison across traditions")
    cross_tradition_analysis: Optional[str] = Field(None, description="Analysis of similarities and differences")
    commonalities: Optional[List[str]] = Field(None, description="Common elements across traditions")
    unique_elements: Optional[Dict[str, List[str]]] = Field(None, description="Unique elements by tradition")
    
    # Common fields
    sources: List[Dict[str, str]] = Field([], description="Source citations for the response")

class TraditionList(BaseModel):
    """Model for list of available traditions"""
    traditions: List[str] = Field(..., description="List of available religious traditions")

class TimePeriodList(BaseModel):
    """Model for list of available time periods"""
    time_periods: List[str] = Field(..., description="List of available time periods")
