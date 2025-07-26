import os
import logging
import sys
sys.path.append('/home/runner/workspace')
from typing import Dict, List, Optional, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from offline_search_engine import OfflineSearchEngine, SearchResult

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingStore:
    """
    Class for managing document embeddings and vector search using ChromaDB
    """
    def __init__(
        self,
        persist_directory: str = "./data/chromadb",
        embedding_model_name: str = "text-embedding-3-small"
    ):
        """
        Initialize the EmbeddingStore
        
        Args:
            persist_directory: Directory to persist the ChromaDB vector store
            embedding_model_name: OpenAI embedding model to use
        """
        self.persist_directory = persist_directory
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize the embedding function
        self.embedding_model = OpenAIEmbeddings(
            model=embedding_model_name
        )
        
        # Initialize ChromaDB
        self._initialize_chroma()
        
        # Initialize offline search engine as fallback
        self.offline_engine = OfflineSearchEngine()
    
    def _initialize_chroma(self):
        """Initialize ChromaDB vector store"""
        try:
            # Try to load existing vector store
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model
            )
            logger.info(f"Loaded existing ChromaDB from {self.persist_directory}")
        except Exception as e:
            logger.warning(f"Could not load existing ChromaDB: {str(e)}")
            # Create new vector store
            self.db = Chroma(
                embedding_function=self.embedding_model,
                persist_directory=self.persist_directory
            )
            logger.info(f"Created new ChromaDB instance at {self.persist_directory}")
    
    def is_populated(self) -> bool:
        """Check if the vector store has documents"""
        return self.db._collection.count() > 0
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            logger.warning("No documents provided to add_documents")
            return
        
        try:
            self.db.add_documents(documents)
            # Persist to disk
            self.db.persist()
            logger.info(f"Added {len(documents)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {str(e)}")
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform similarity search on the vector store
        
        Args:
            query: Query string
            k: Number of results to return
            filter: Filter to apply to the search
        
        Returns:
            List of documents similar to the query
        """
        try:
            results = self.db.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []
    
    def search_by_tradition(
        self,
        query: str,
        tradition: str,
        k: int = 5,
        text_type: Optional[str] = None
    ) -> List[Document]:
        """
        Search for documents from a specific religious tradition
        
        Args:
            query: Query string
            tradition: Religious tradition to filter by
            k: Number of results to return
            text_type: Type of text (original, commentary, modern)
        
        Returns:
            List of relevant documents
        """
        filter_dict = {"tradition": tradition}
        
        if text_type:
            filter_dict["text_type"] = text_type
        
        return self.similarity_search(query, k, filter_dict)
    
    def search_by_time_period(
        self,
        query: str,
        time_period: str,
        k: int = 5,
        tradition: Optional[str] = None
    ) -> List[Document]:
        """
        Search for documents from a specific time period
        
        Args:
            query: Query string
            time_period: Time period to filter by
            k: Number of results to return
            tradition: Optional religious tradition to filter by
        
        Returns:
            List of relevant documents
        """
        filter_dict = {"time_period": time_period}
        
        if tradition:
            filter_dict["tradition"] = tradition
        
        return self.similarity_search(query, k, filter_dict)
    
    def get_original_teachings(
        self,
        query: str,
        tradition: str,
        k: int = 3
    ) -> List[Document]:
        """
        Get original teachings for a specific query and tradition
        
        Args:
            query: Query string
            tradition: Religious tradition
            k: Number of results to return
        
        Returns:
            List of documents containing original teachings
        """
        return self.search_by_tradition(
            query=query,
            tradition=tradition,
            k=k,
            text_type="original"
        )
    
    def get_modern_interpretations(
        self,
        query: str,
        tradition: str,
        k: int = 3
    ) -> List[Document]:
        """
        Get modern interpretations for a specific query and tradition
        
        Args:
            query: Query string
            tradition: Religious tradition
            k: Number of results to return
        
        Returns:
            List of documents containing modern interpretations
        """
        # Try to find documents explicitly marked as modern
        modern_docs = self.search_by_tradition(
            query=query,
            tradition=tradition,
            k=k,
            text_type="modern"
        )
        
        # If not enough modern docs, look for commentaries
        if len(modern_docs) < k:
            commentaries = self.search_by_tradition(
                query=query,
                tradition=tradition,
                k=k - len(modern_docs),
                text_type="commentary"
            )
            modern_docs.extend(commentaries)
        
        return modern_docs[:k]
