import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import re
import json

from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    PyPDFLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentLoader:
    """
    Class for loading, processing, and chunking religious texts from various sources
    """
    def __init__(
        self,
        corpus_path: str = "./data/texts",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the DocumentLoader
        
        Args:
            corpus_path: Path to the directory containing the religious texts
            chunk_size: Size of document chunks for embedding
            chunk_overlap: Overlap between chunks for context preservation
        """
        self.corpus_path = corpus_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        
        # Validate corpus path
        corpus_dir = Path(corpus_path)
        if not corpus_dir.exists():
            logger.info(f"Corpus directory {corpus_path} does not exist. Creating it.")
            corpus_dir.mkdir(parents=True, exist_ok=True)
    
    def load_documents(self) -> List[Document]:
        """
        Load all documents from the corpus directory
        
        Returns:
            List of loaded and processed documents
        """
        corpus_dir = Path(self.corpus_path)
        
        # Check if corpus directory exists
        if not corpus_dir.exists():
            logger.warning(f"Corpus directory {self.corpus_path} does not exist.")
            return []
        
        documents = []
        
        # Walk through the corpus directory to find all text files
        for root, dirs, files in os.walk(corpus_dir):
            for file in files:
                file_path = Path(root) / file
                
                # Skip metadata files and README files
                if file.startswith('.') or file == 'README.md':
                    continue
                
                try:
                    # Load documents based on file extension
                    if file.endswith('.txt'):
                        doc = self._load_text_file(file_path)
                        documents.extend(doc)
                    elif file.endswith('.pdf'):
                        doc = self._load_pdf_file(file_path)
                        documents.extend(doc)
                    elif file.endswith('.json'):
                        doc = self._load_json_file(file_path)
                        documents.extend(doc)
                except Exception as e:
                    logger.error(f"Error loading file {file_path}: {str(e)}")
        
        logger.info(f"Loaded {len(documents)} documents from {self.corpus_path}")
        
        # Split documents into chunks
        chunked_documents = self._chunk_documents(documents)
        logger.info(f"Created {len(chunked_documents)} chunks from {len(documents)} documents")
        
        # Enrich document metadata
        enriched_documents = self._enrich_metadata(chunked_documents)
        
        return enriched_documents
    
    def _load_text_file(self, file_path: Path) -> List[Document]:
        """Load a text file and create a Document object"""
        logger.info(f"Loading text file: {file_path}")
        loader = TextLoader(file_path, encoding="utf-8")
        return self._process_file(loader.load(), file_path)

    def _load_pdf_file(self, file_path: Path) -> List[Document]:
        """Load a PDF file and create Document objects"""
        logger.info(f"Loading PDF file: {file_path}")
        loader = PyPDFLoader(str(file_path))
        return self._process_file(loader.load(), file_path)
    
    def _load_json_file(self, file_path: Path) -> List[Document]:
        """Load a JSON file with text content and create Document objects"""
        logger.info(f"Loading JSON file: {file_path}")
        documents = []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Handle different JSON formats
                if isinstance(data, list):
                    for item in data:
                        if "text" in item:
                            doc = Document(
                                page_content=item["text"],
                                metadata=item.get("metadata", {})
                            )
                            documents.append(doc)
                elif isinstance(data, dict):
                    if "text" in data:
                        doc = Document(
                            page_content=data["text"],
                            metadata=data.get("metadata", {})
                        )
                        documents.append(doc)
                    elif "sections" in data:
                        for section in data["sections"]:
                            if "text" in section:
                                doc = Document(
                                    page_content=section["text"],
                                    metadata=section.get("metadata", {})
                                )
                                documents.append(doc)
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
            
        return self._process_file(documents, file_path)
    
    def _process_file(self, documents: List[Document], file_path: Path) -> List[Document]:
        """Process loaded documents to extract and add metadata"""
        # Extract metadata from file path
        rel_path = file_path.relative_to(self.corpus_path)
        path_parts = list(rel_path.parts)
        
        # File is directly in corpus directory
        if len(path_parts) == 1:
            tradition = "Unknown"
            time_period = "Unknown"
            text_name = Path(path_parts[0]).stem
        # File is in a subdirectory structure
        elif len(path_parts) >= 2:
            tradition = path_parts[0]
            if len(path_parts) >= 3:
                time_period = path_parts[1]
                text_name = str(Path(*path_parts[2:]).stem)
            else:
                time_period = "Unknown"
                text_name = Path(path_parts[1]).stem
        
        # Update metadata for each document
        for doc in documents:
            # Initialize metadata if it doesn't exist
            if not hasattr(doc, 'metadata') or doc.metadata is None:
                doc.metadata = {}
            
            # Add basic metadata
            doc.metadata.update({
                "source": str(file_path),
                "file_name": file_path.name,
                "tradition": tradition,
                "time_period": time_period,
                "text_name": text_name
            })
        
        return documents
    
    def _chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks of specified size"""
        chunked_docs = []
        for doc in documents:
            try:
                chunks = self.text_splitter.split_documents([doc])
                chunked_docs.extend(chunks)
            except Exception as e:
                logger.error(f"Error splitting document: {str(e)}")
                # Include the original document if splitting fails
                chunked_docs.append(doc)
        
        return chunked_docs
    
    def _enrich_metadata(self, documents: List[Document]) -> List[Document]:
        """Enhance document metadata with additional information"""
        for doc in documents:
            # Extract year ranges from time periods
            if "time_period" in doc.metadata:
                time_period = doc.metadata["time_period"]
                year_range = self._extract_year_range(time_period)
                if year_range:
                    doc.metadata["year_start"] = year_range[0]
                    doc.metadata["year_end"] = year_range[1]
            
            # Categorize documents as original, interpretations, or commentaries
            file_path = doc.metadata.get("source", "")
            file_name = doc.metadata.get("file_name", "").lower()
            
            if any(term in file_name for term in ["original", "source", "ancient"]):
                doc.metadata["text_type"] = "original"
            elif any(term in file_name for term in ["commentary", "interpret", "analysis"]):
                doc.metadata["text_type"] = "commentary"
            elif any(term in file_name for term in ["modern", "contemporary"]):
                doc.metadata["text_type"] = "modern"
            else:
                # Default to original if not specified
                doc.metadata["text_type"] = "unknown"
        
        return documents
    
    def _extract_year_range(self, time_period: str) -> Optional[tuple]:
        """
        Extract year range from time period string
        
        Examples:
            "Ancient (3000-1000 BCE)" -> (-3000, -1000)
            "Modern (1800-1950 CE)" -> (1800, 1950)
        """
        try:
            # Match patterns like "Period (YYYY-YYYY BCE/CE)"
            match = re.search(r'(\d+)[^\d]+(\d+)[^\d]+(BCE|BC|CE|AD)', time_period, re.IGNORECASE)
            if match:
                start_year = int(match.group(1))
                end_year = int(match.group(2))
                era = match.group(3).upper()
                
                # Convert BCE/BC years to negative numbers
                if era in ["BCE", "BC"]:
                    start_year = -start_year
                    end_year = -end_year
                
                return (start_year, end_year)
            return None
        except:
            return None
