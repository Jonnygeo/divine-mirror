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
            
            # Check if we need to use fallback response
            if result.get("needs_fallback"):
                logger.info("Smart model returned needs_fallback flag, using fallback response")
                return self._get_fallback_response(question, traditions)
            
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
            # Return enhanced fallback response using truth analysis
            return self._get_fallback_response(question, traditions)
    
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
            # Return enhanced fallback response
            return self._get_fallback_response(question, traditions)
    
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
            # Return enhanced fallback response
            return self._get_fallback_response(question, traditions)
    
    def _get_fallback_response(self, question: str, traditions: List[str]) -> QueryResponse:
        """Enhanced fallback response using comprehensive truth analysis"""
        question_lower = question.lower()
        
        # Kingdom within responses
        if any(keyword in question_lower for keyword in ['kingdom', 'god', 'heaven', 'within']):
            return QueryResponse(
                original_teachings="According to Yeshua's original teachings, the Kingdom of God is within you (Luke 17:21). As recorded in the Gospel of Thomas (Saying 3): 'The Kingdom is inside you and outside you. If you know yourselves, then you will be known.' This inner spiritual state is accessible through direct divine awareness, bypassing religious intermediaries.",
                modern_interpretations="Modern Christianity externalized the Kingdom into physical churches, sacramental systems, and institutional hierarchy. The Vatican claims exclusive access to God through priestly mediation, contradicting Yeshua's clear teaching of inner divine connection.",
                comparison="Original: Direct inner spiritual access vs. Modern: Institutional dependency and external control",
                key_differences=[
                    "Original taught inner divine awareness - Modern requires external mediation",
                    "Original emphasized personal spiritual responsibility - Modern creates institutional dependency", 
                    "Original message was universal accessibility - Modern restricts through doctrine and hierarchy"
                ],
                sources=[
                    {"title": "Luke 17:21", "tradition": "Christianity", "period": "Classical", "citation": "Kingdom of God is within you", "relevance": "Core teaching about inner divine access"},
                    {"title": "Gospel of Thomas Saying 3", "tradition": "Gnosticism", "period": "Classical", "citation": "The Kingdom is inside you and outside you", "relevance": "Preserved original understanding"}
                ]
            )
        
        # Hell deception responses  
        elif any(keyword in question_lower for keyword in ['hell', 'eternal', 'punishment', 'damnation']):
            return QueryResponse(
                original_teachings="Original Hebrew 'Sheol' meant 'grave' or 'place of the dead.' Greek 'Hades' meant the same. 'Gehenna' referred to the Valley of Hinnom, Jerusalem's literal garbage dump. 'Eternal' (aionios) means 'age-lasting,' not infinite. Yeshua used Gehenna as metaphor for spiritual consequence.",
                modern_interpretations="Latin translators conflated Sheol, Hades, and Gehenna into 'infernus' to create fear-based control. Church councils amplified hell doctrine to create institutional dependency through terror rather than encouraging direct divine relationship.",
                comparison="Original: Metaphorical teaching about spiritual consequences vs. Modern: Literal eternal torture for control",
                key_differences=[
                    "Original used Gehenna as metaphor for waste/consequence - Modern teaches literal eternal torture",
                    "Original 'aionios' meant age-lasting - Modern mistranslates as infinite",
                    "Original focused on spiritual transformation - Modern uses fear for institutional control"
                ],
                sources=[
                    {"title": "Hebrew Sheol Analysis", "tradition": "Judaism", "period": "Ancient", "citation": "Place of the dead, not torture", "relevance": "Original meaning before mistranslation"},
                    {"title": "Greek Hades Definition", "tradition": "Christianity", "period": "Classical", "citation": "Underworld, place of departed souls", "relevance": "Pre-Latin translation meaning"}
                ]
            )
        
        # Truth vs control themes
        elif any(keyword in question_lower for keyword in ['truth', 'control', 'manipulation', 'church']):
            return QueryResponse(
                original_teachings="Yeshua taught 'You will know the truth, and the truth will set you free' (John 8:32), emphasizing liberation through direct knowledge of God. He rejected hierarchical titles, saying 'You have one Teacher, and you are all brothers' (Matthew 23:8-10).",
                modern_interpretations="Post-Constantine Christianity centralized authority through papal supremacy and sacramental control. The Council of Nicaea (325 CE) prioritized institutional control over Yeshua's original message of spiritual freedom.",
                comparison="Original: Truth brings freedom vs. Modern: Institution controls truth",
                key_differences=[
                    "Original emphasized direct divine knowledge - Modern requires clerical interpretation",
                    "Original rejected hierarchical titles - Modern created elaborate religious hierarchy",
                    "Original taught spiritual liberation - Modern created institutional dependency"
                ],
                sources=[
                    {"title": "John 8:32", "tradition": "Christianity", "period": "Classical", "citation": "Truth will set you free", "relevance": "Core liberation teaching"},
                    {"title": "Matthew 23:8-10", "tradition": "Christianity", "period": "Classical", "citation": "Rejection of religious hierarchy", "relevance": "Anti-institutional message"}
                ]
            )
        
        # General spiritual analysis
        else:
            return QueryResponse(
                original_teachings="Original spiritual teachings across traditions emphasize direct personal connection with the divine, inner wisdom, and spiritual transformation. Core principles include love, compassion, and personal spiritual responsibility.",
                modern_interpretations="Modern religious institutions often externalize spiritual authority, create dependency through intermediaries, and emphasize compliance over personal spiritual growth.",
                comparison="Original teachings empower individual spiritual development while modern interpretations often centralize control through institutional authority.",
                key_differences=[
                    "Original: Direct spiritual access - Modern: Mediated through institutions",
                    "Original: Personal responsibility - Modern: Institutional dependency",
                    "Original: Universal love - Modern: Conditional acceptance"
                ],
                sources=[
                    {"title": "Comprehensive Truth Analysis", "tradition": "Multi-tradition", "period": "All", "citation": "JonnyG's Bible Dissection Project", "relevance": "Complete institutional manipulation analysis"}
                ]
            )