import os
import logging
import json
from typing import Dict, List, Any, Optional

from openai import OpenAI
from langchain.chains import LLMChain as LangChainLLM
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
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
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def _format_documents_for_prompt(self, documents: List[Document]) -> str:
        """Format documents for inclusion in a prompt"""
        if not documents:
            return "No relevant documents found."
        
        formatted_docs = []
        for i, doc in enumerate(documents):
            # Format metadata for readability
            metadata = doc.metadata
            source = f"{metadata.get('text_name', 'Unknown Text')}"
            if metadata.get('tradition'):
                source += f" ({metadata.get('tradition')})"
            if metadata.get('time_period'):
                source += f", {metadata.get('time_period')}"
            
            formatted_doc = f"Document {i+1} from {source}:\n{doc.page_content}\n"
            formatted_docs.append(formatted_doc)
        
        return "\n".join(formatted_docs)
    
    def _get_system_prompt(self) -> str:
        """Get the base system prompt for ethical and unbiased analysis"""
        return """You are Divine Mirror AI, an expert scholar of comparative religion, ancient languages, and historical spiritual texts. Your purpose is to provide objective, scholarly insights into religious and spiritual teachings across different traditions and time periods.

Follow these guidelines:
1. Remain strictly neutral and unbiased in your analysis
2. Do not promote any specific religion or spiritual belief system
3. Base your responses solely on scholarly research and authentic religious texts
4. Distinguish clearly between original teachings and later interpretations or additions
5. Provide historical context for how teachings have evolved over time
6. When similarities exist across traditions, present them factually without implying syncretism
7. Respect the integrity of each tradition's unique worldview and terminology
8. Always cite your sources and acknowledge limitations in available historical evidence
9. Use precise, accurate terminology specific to each tradition
10. Avoid simplistic generalizations that might misrepresent complex spiritual concepts

Present information clearly, accurately, and with appropriate academic context. Your goal is to illuminate the original meanings of spiritual teachings and trace how they may have changed through history."""
    
    def _get_traditions_info(self, traditions: List[str]) -> str:
        """Get information about selected traditions"""
        if not traditions:
            return ""
            
        return f"The queried traditions are: {', '.join(traditions)}."
    
    def _construct_source_citations(self, documents: List[Document]) -> List[Dict[str, str]]:
        """Create source citations from document metadata"""
        sources = []
        
        for doc in documents:
            metadata = doc.metadata
            citation = {
                "title": metadata.get("text_name", "Unknown Text"),
                "tradition": metadata.get("tradition", "Unknown Tradition"),
                "period": metadata.get("time_period", "Unknown Period"),
                "text_type": metadata.get("text_type", "unknown"),
                "citation": f"{metadata.get('text_name', 'Unknown Text')}, {metadata.get('tradition', 'Unknown')}, {metadata.get('time_period', 'Unknown Period')}",
                "relevance": "This source contains relevant information about the query."
            }
            sources.append(citation)
        
        return sources
    
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
        all_documents = []
        
        # Retrieve relevant documents for each tradition
        for tradition in traditions:
            # Get original teachings
            original_docs = self.embedding_store.get_original_teachings(
                query=question,
                tradition=tradition,
                k=3
            )
            
            # Get modern interpretations
            modern_docs = self.embedding_store.get_modern_interpretations(
                query=question,
                tradition=tradition,
                k=3
            )
            
            all_documents.extend(original_docs)
            all_documents.extend(modern_docs)
        
        # Format documents for prompt
        formatted_docs = self._format_documents_for_prompt(all_documents)
        
        # Construct comparison prompt
        prompt = f"""
System: {self._get_system_prompt()}

User: I'd like to understand how original spiritual teachings compare with modern interpretations regarding this question: "{question}"

{self._get_traditions_info(traditions)}

Here are relevant passages from original texts and modern interpretations:

{formatted_docs}

Please provide:
1. A detailed summary of the original teachings on this topic
2. An explanation of modern interpretations and how they differ
3. A clear comparison highlighting key differences and potential reasons for the evolution of these teachings
4. A bullet-point list of the most significant differences between original and modern understandings
5. Citations for the sources you used

Format your response as JSON with these keys:
- original_teachings: detailed summary of original teachings
- modern_interpretations: summary of modern interpretations
- comparison: analysis of how and why the teachings changed
- key_differences: array of bullet points listing major differences
- sources: array of source citations used in your analysis
"""
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            result = json.loads(response_text)
            
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
        all_documents = []
        
        # Retrieve relevant documents for each tradition and time period
        for tradition in traditions:
            for time_period in time_periods:
                period_docs = self.embedding_store.search_by_time_period(
                    query=question,
                    time_period=time_period,
                    tradition=tradition,
                    k=2
                )
                all_documents.extend(period_docs)
        
        # Format documents for prompt
        formatted_docs = self._format_documents_for_prompt(all_documents)
        
        # Construct timeline prompt
        prompt = f"""
System: {self._get_system_prompt()}

User: I'd like to understand how spiritual teachings about this topic have evolved over time: "{question}"

{self._get_traditions_info(traditions)}

The time periods I'm interested in are: {', '.join(time_periods)}

Here are relevant passages from texts across these time periods:

{formatted_docs}

Please provide:
1. An analysis of how teachings on this topic evolved through each time period
2. Key concepts that remained consistent and those that changed over time
3. A timeline showing the evolution of these teachings
4. An explanation of historical, cultural, or theological factors that influenced these changes
5. Citations for the sources you used

Format your response as JSON with these keys:
- evolution_analysis: detailed analysis of how the teaching evolved
- timeline_data: array of objects for each time period with structure:
  - period: name of time period
  - description: teachings during this period
  - key_concepts: array of main concepts from this period
  - key_texts: array of important texts from this period
- sources: array of source citations used in your analysis
"""
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            result = json.loads(response_text)
            
            # Format sources correctly
            source_citations = self._construct_source_citations(all_documents)
            
            # Construct response object with timeline data
            query_response = QueryResponse(
                evolution_analysis=result.get("evolution_analysis", ""),
                timeline_data=result.get("timeline_data", []),
                sources=source_citations
            )
            
            return query_response
        
        except Exception as e:
            logger.error(f"Error in compare_across_time_periods: {str(e)}")
            # Return basic error response
            return QueryResponse(
                evolution_analysis="Error retrieving evolution analysis.",
                timeline_data=[],
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
        all_documents = []
        tradition_docs = {}
        
        # Retrieve relevant documents for each tradition
        for tradition in traditions:
            tradition_specific_docs = self.embedding_store.search_by_tradition(
                query=question,
                tradition=tradition,
                k=4
            )
            tradition_docs[tradition] = tradition_specific_docs
            all_documents.extend(tradition_specific_docs)
        
        # Format all documents for prompt
        formatted_docs = self._format_documents_for_prompt(all_documents)
        
        # Format each tradition's documents separately
        traditions_formatted = {}
        for tradition, docs in tradition_docs.items():
            traditions_formatted[tradition] = self._format_documents_for_prompt(docs)
        
        # Construct cross-tradition prompt
        prompt = f"""
System: {self._get_system_prompt()}

User: I'd like to compare how different spiritual traditions approach this topic: "{question}"

The traditions I'm comparing are: {', '.join(traditions)}

Here are relevant passages from texts in these traditions:

{formatted_docs}

Please provide:
1. A detailed analysis for each tradition's perspective on this topic
2. A comparative analysis highlighting similarities and differences
3. Common theological or philosophical elements shared across traditions
4. Unique elements specific to each tradition
5. Citations for the sources you used

Format your response as JSON with these keys:
- traditions_comparison: object with each tradition name as key and their perspective as value
- cross_tradition_analysis: comparative analysis of similarities and differences
- commonalities: array of common elements shared across traditions
- unique_elements: object with each tradition name as key and array of unique elements as value
- sources: array of source citations used in your analysis
"""
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            result = json.loads(response_text)
            
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
                cross_tradition_analysis="Error retrieving cross-tradition analysis.",
                commonalities=[],
                unique_elements={},
                sources=[]
            )
