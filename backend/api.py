from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from backend.model import (
    QueryRequest, 
    QueryResponse, 
    TraditionList, 
    TimePeriodList, 
    SourceCitation
)
from backend.document_loader import DocumentLoader
from backend.embedding_store import EmbeddingStore
from backend.llm_chain import LLMChain
from backend.utils import load_environment_variables

# Load environment variables
load_environment_variables()

# Initialize FastAPI app
app = FastAPI(
    title="Divine Mirror AI API",
    description="API for comparing spiritual truths across religions and time periods",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up global components
CORPUS_PATH = os.getenv("CORPUS_PATH", "./data/texts")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chromadb")

# Initialize components lazily to prevent startup delay
document_loader = None
embedding_store = None
llm_chain = None

# Flag to track initialization status
is_initialized = False

def get_document_loader():
    global document_loader
    if document_loader is None:
        document_loader = DocumentLoader(corpus_path=CORPUS_PATH)
    return document_loader

def get_embedding_store():
    global embedding_store
    if embedding_store is None:
        embedding_store = EmbeddingStore(persist_directory=CHROMA_DB_PATH)
    return embedding_store

def get_llm_chain():
    global llm_chain
    if llm_chain is None:
        llm_chain = LLMChain(embedding_store=get_embedding_store())
    return llm_chain

def initialize_system(background_tasks: BackgroundTasks):
    """Initialize the system components if not already done"""
    global is_initialized
    
    if not is_initialized:
        # Add initialization tasks to run in the background
        background_tasks.add_task(_initialize_corpus_and_embeddings)

async def _initialize_corpus_and_embeddings():
    """Background task to initialize corpus and embeddings"""
    global is_initialized
    
    try:
        # Get the components (this will initialize them if not already done)
        document_loader = get_document_loader()
        embedding_store = get_embedding_store()
        
        # Load the corpus if not already loaded
        if not embedding_store.is_populated():
            # Load documents
            documents = document_loader.load_documents()
            
            # Process and store documents
            embedding_store.add_documents(documents)
        
        is_initialized = True
    except Exception as e:
        print(f"Error during initialization: {str(e)}")

# Available religious traditions
AVAILABLE_TRADITIONS = [
    "Christianity", 
    "Islam", 
    "Judaism", 
    "Hinduism", 
    "Buddhism", 
    "Taoism", 
    "Zoroastrianism",
    "Gnosticism",
    "Hermeticism",
    "Ancient Egyptian Religion",
    "Greek and Roman Religion",
    "Indigenous Traditions"
]

# Available time periods
AVAILABLE_TIME_PERIODS = [
    "Ancient (3000-1000 BCE)",
    "Classical (1000 BCE-500 CE)",
    "Medieval (500-1500 CE)",
    "Early Modern (1500-1800 CE)",
    "Modern (1800-1950 CE)",
    "Contemporary (1950-Present)"
]

@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    # Load environment variables (already done above, but just to be safe)
    load_environment_variables()

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint to check if the API is running"""
    return {"message": "Divine Mirror AI API is running", "status": "healthy"}

@app.get("/traditions", response_model=TraditionList, tags=["Reference Data"])
async def get_traditions(background_tasks: BackgroundTasks):
    """Get available religious traditions"""
    # Initialize system if not already done
    initialize_system(background_tasks)
    
    return {"traditions": AVAILABLE_TRADITIONS}

@app.get("/time_periods", response_model=TimePeriodList, tags=["Reference Data"])
async def get_time_periods(background_tasks: BackgroundTasks):
    """Get available time periods for comparison"""
    # Initialize system if not already done
    initialize_system(background_tasks)
    
    return {"time_periods": AVAILABLE_TIME_PERIODS}

@app.post("/query", response_model=QueryResponse, tags=["Queries"])
async def query_spiritual_truth(
    request: QueryRequest,
    background_tasks: BackgroundTasks
):
    """
    Query for spiritual truths across different traditions and time periods
    """
    # Initialize system if not already done
    initialize_system(background_tasks)
    
    # Validate request
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if not request.traditions:
        raise HTTPException(status_code=400, detail="At least one tradition must be selected")
    
    if request.comparison_mode == "across_time_periods" and not request.time_periods:
        raise HTTPException(status_code=400, detail="Time periods must be provided for across_time_periods mode")
    
    try:
        # Process the query
        llm_chain = get_llm_chain()
        
        # Generate response based on comparison mode
        if request.comparison_mode == "modern_vs_original":
            response = llm_chain.compare_modern_vs_original(
                question=request.question,
                traditions=request.traditions
            )
        elif request.comparison_mode == "across_time_periods":
            response = llm_chain.compare_across_time_periods(
                question=request.question,
                traditions=request.traditions,
                time_periods=request.time_periods
            )
        else:  # across_traditions
            response = llm_chain.compare_across_traditions(
                question=request.question,
                traditions=request.traditions
            )
        
        # Only use fallback if there's a genuine system error, not empty content
        # The LLM should handle empty results internally and provide analysis
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/system/status", tags=["System"])
async def get_system_status(background_tasks: BackgroundTasks):
    """Get system initialization status"""
    # Try to initialize if not already done
    initialize_system(background_tasks)
    
    return {
        "initialized": is_initialized,
        "corpus_path": CORPUS_PATH,
        "chroma_db_path": CHROMA_DB_PATH
    }

@app.get("/test_smart_model")
async def test_smart_model():
    """Test the smart model switcher"""
    from backend.smart_response import smart_generate
    
    test_prompt = "Explain the Kingdom of God as a spiritual state according to Jesus's original teachings."
    
    try:
        response = smart_generate(test_prompt, max_tokens=300)
        return {
            "status": "success",
            "prompt": test_prompt,
            "response": response,
            "model": "Smart Model Switcher (OpenAI with DeepSeek fallback)"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "prompt": test_prompt
        }

def start():
    """Run the API server with Uvicorn"""
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
