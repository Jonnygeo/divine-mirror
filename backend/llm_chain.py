import os
import logging
import json
from typing import Dict, List, Any, Optional

from langchain.schema import Document

from backend.embedding_store import EmbeddingStore
from backend.model import QueryResponse, SourceCitation
from backend.smart_response import smart_generate, smart_generate_json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMChain:
    """
    Class for handling LLM operations including prompt construction, 
    API calls, and response formatting.
    """
    def __init__(
        self,
        embedding_store: EmbeddingStore,
        model_name: str = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    ):
        """
        Initialize the LLM Chain
        
        Args:
            embedding_store: Instance of EmbeddingStore for retrieving relevant documents
            model_name: Name of the OpenAI model to use
        """
        self.embedding_store = embedding_store
        self.model_name = model_name
        
        logger.info(f"Initialized LLMChain with model: {model_name}")
    
    def _format_documents_for_prompt(self, documents: List[Document]) -> str:
        """Format documents for inclusion in a prompt"""
        formatted_docs = []
        for doc in documents:
            metadata = doc.metadata
            formatted_doc = f"""
Source: {metadata.get('title', 'Unknown')}
Tradition: {metadata.get('tradition', 'Unknown')}
Period: {metadata.get('period', 'Unknown')}
Type: {metadata.get('text_type', 'Unknown')}
Content: {doc.page_content}
---
"""
            formatted_docs.append(formatted_doc)
        
        return "\n".join(formatted_docs)
    
    def _get_system_prompt(self) -> str:
        """Get the base system prompt for ethical and unbiased analysis"""
        return """You are a scholarly religious studies expert analyzing historical and contemporary religious texts. Your role is to provide objective, evidence-based comparisons between original teachings and modern interpretations.

Guidelines:
- Maintain scholarly objectivity and avoid bias
- Present multiple perspectives when they exist
- Acknowledge uncertainty when evidence is limited
- Focus on historical context and textual evidence
- Avoid making definitive claims about religious truth
- Respect all religious traditions while examining them critically
- Always provide source citations for your analysis

Respond only in valid JSON format with the required fields."""
    
    def _get_traditions_info(self, traditions: List[str]) -> str:
        """Get information about selected traditions"""
        tradition_info = {
            "Christianity": "Focus on Jesus's original teachings versus modern church doctrine",
            "Buddhism": "Compare Buddha's original teachings with modern Buddhist practices",
            "Islam": "Examine Quranic teachings versus contemporary Islamic interpretations",
            "Judaism": "Analyze Torah and Talmudic teachings versus modern Jewish practices",
            "Taoism": "Compare Lao Tzu's original Tao Te Ching with modern Taoist practices",
            "Hinduism": "Examine Vedic texts versus contemporary Hindu practices",
            "Gnosticism": "Ancient Gnostic texts and their alternative Christian interpretations",
            "Hermeticism": "Hermetic principles and their influence on Western esoteric traditions"
        }
        
        selected_info = []
        for tradition in traditions:
            if tradition in tradition_info:
                selected_info.append(f"{tradition}: {tradition_info[tradition]}")
        
        return "\n".join(selected_info)
    
    def _construct_source_citations(self, documents: List[Document]) -> List[Dict[str, str]]:
        """Create source citations from document metadata"""
        citations = []
        for doc in documents:
            metadata = doc.metadata
            citation = {
                "title": metadata.get('title', 'Unknown Source'),
                "tradition": metadata.get('tradition', 'Unknown'),
                "period": metadata.get('period', 'Unknown'),
                "text_type": metadata.get('text_type', 'Unknown'),
                "citation": f"{metadata.get('title', 'Unknown')} - {metadata.get('tradition', 'Unknown')} ({metadata.get('period', 'Unknown')})"
            }
            citations.append(citation)
        
        return citations
    
    def compare_modern_vs_original(
        self,
        question: str,
        traditions: List[str]
    ) -> QueryResponse:
        """
        Compare modern interpretations with original teachings across selected traditions
        
        Args:
            question: User's question about spiritual truth
            traditions: List of religious traditions to query
        
        Returns:
            QueryResponse with comparison between original and modern teachings
        """
        # Get relevant documents
        all_documents = []
        for tradition in traditions:
            # Get original teachings
            original_docs = self.embedding_store.get_original_teachings(
                question, tradition, k=3
            )
            all_documents.extend(original_docs)
            
            # Get modern interpretations
            modern_docs = self.embedding_store.get_modern_interpretations(
                question, tradition, k=3
            )
            all_documents.extend(modern_docs)
        
        # Format documents for prompt
        formatted_docs = self._format_documents_for_prompt(all_documents)
        traditions_info = self._get_traditions_info(traditions)
        
        # Create prompt
        prompt = f"""
{self._get_system_prompt()}

Question: {question}

Traditions to analyze: {', '.join(traditions)}

{traditions_info}

Relevant source material:
{formatted_docs}

Provide a comprehensive comparison between original teachings and modern interpretations. Return your response in JSON format with these fields:
- original_teachings: Summary of what the original sources say
- modern_interpretations: Summary of how modern institutions interpret this
- comparison: Detailed comparison highlighting differences and similarities
- key_differences: Array of key differences as bullet points

Focus on historical accuracy and scholarly analysis."""
        
        try:
            # Call Smart Model Switcher (OpenAI with DeepSeek fallback)
            result = smart_generate_json(prompt, model=self.model_name, max_tokens=2000)
            
            # Format sources correctly
            source_citations = self._construct_source_citations(all_documents)
            
            # Construct response object
            query_response = QueryResponse(
                original_teachings=result.get("original_teachings", ""),
                modern_interpretations=result.get("modern_interpretations", ""),
                comparison=result.get("comparison", ""),
                key_differences=result.get("key_differences", []),
                sources=source_citations
            )
            
            return query_response
        
        except Exception as e:
            logger.error(f"Error in compare_modern_vs_original: {str(e)}")
            # Return basic error response
            return QueryResponse(
                original_teachings="Error retrieving original teachings.",
                modern_interpretations="Error retrieving modern interpretations.",
                comparison="Unable to generate comparison due to an error.",
                key_differences=[],
                sources=[]
            )
    
    def compare_across_time_periods(
        self,
        question: str,
        traditions: List[str],
        time_periods: List[str]
    ) -> QueryResponse:
        """
        Compare teachings across different time periods
        
        Args:
            question: User's question about spiritual truth
            traditions: List of religious traditions to query
            time_periods: List of time periods to compare
        
        Returns:
            QueryResponse with timeline analysis
        """
        # Get relevant documents for each time period
        all_documents = []
        for period in time_periods:
            for tradition in traditions:
                period_docs = self.embedding_store.search_by_time_period(
                    question, period, k=3, tradition=tradition
                )
                all_documents.extend(period_docs)
        
        # Format documents for prompt
        formatted_docs = self._format_documents_for_prompt(all_documents)
        traditions_info = self._get_traditions_info(traditions)
        
        # Create prompt
        prompt = f"""
{self._get_system_prompt()}

Question: {question}

Traditions to analyze: {', '.join(traditions)}
Time periods to compare: {', '.join(time_periods)}

{traditions_info}

Relevant source material:
{formatted_docs}

Analyze how teachings evolved across these time periods. Return your response in JSON format with these fields:
- evolution_analysis: How the teachings changed over time
- timeline_data: Array of objects with period, key_teachings, and context for each time period
- comparison: Overall comparison across time periods
- key_differences: Array of key evolutionary changes

Focus on historical development and contextual changes."""
        
        try:
            # Call Smart Model Switcher (OpenAI with DeepSeek fallback)
            result = smart_generate_json(prompt, model=self.model_name, max_tokens=2000)
            
            # Format sources correctly
            source_citations = self._construct_source_citations(all_documents)
            
            # Construct response object
            query_response = QueryResponse(
                evolution_analysis=result.get("evolution_analysis", ""),
                timeline_data=result.get("timeline_data", []),
                comparison=result.get("comparison", ""),
                key_differences=result.get("key_differences", []),
                sources=source_citations
            )
            
            return query_response
        
        except Exception as e:
            logger.error(f"Error in compare_across_time_periods: {str(e)}")
            # Return basic error response
            return QueryResponse(
                evolution_analysis="Error analyzing timeline evolution.",
                timeline_data=[],
                comparison="Unable to generate timeline comparison due to an error.",
                key_differences=[],
                sources=[]
            )
    
    def compare_across_traditions(
        self,
        question: str,
        traditions: List[str]
    ) -> QueryResponse:
        """
        Compare teachings across different religious traditions
        
        Args:
            question: User's question about spiritual truth
            traditions: List of religious traditions to compare
        
        Returns:
            QueryResponse with cross-tradition analysis
        """
        # Get relevant documents from each tradition
        all_documents = []
        for tradition in traditions:
            tradition_docs = self.embedding_store.search_by_tradition(
                question, tradition, k=4
            )
            all_documents.extend(tradition_docs)
        
        # Format documents for prompt
        formatted_docs = self._format_documents_for_prompt(all_documents)
        traditions_info = self._get_traditions_info(traditions)
        
        # Create prompt
        prompt = f"""
{self._get_system_prompt()}

Question: {question}

Traditions to compare: {', '.join(traditions)}

{traditions_info}

Relevant source material:
{formatted_docs}

Compare how different religious traditions approach this question. Return your response in JSON format with these fields:
- traditions_comparison: Object with each tradition as key and their approach as value
- cross_tradition_analysis: Overall analysis of similarities and differences
- commonalities: Array of common elements across traditions
- unique_elements: Object with each tradition as key and their unique aspects as array values

Focus on respectful comparison and scholarly analysis."""
        
        try:
            # Call Smart Model Switcher (OpenAI with DeepSeek fallback)
            result = smart_generate_json(prompt, model=self.model_name, max_tokens=2000)
            
            # Format sources correctly
            source_citations = self._construct_source_citations(all_documents)
            
            # Construct response object
            query_response = QueryResponse(
                traditions_comparison=result.get("traditions_comparison", {}),
                cross_tradition_analysis=result.get("cross_tradition_analysis", ""),
                commonalities=result.get("commonalities", []),
                unique_elements=result.get("unique_elements", {}),
                sources=source_citations
            )
            
            return query_response
        
        except Exception as e:
            logger.error(f"Error in compare_across_traditions: {str(e)}")
            # Return basic error response
            return QueryResponse(
                traditions_comparison={},
                cross_tradition_analysis="Error analyzing cross-tradition comparison.",
                commonalities=[],
                unique_elements={},
                sources=[]
            )