# Divine Mirror AI - Project Documentation

## Overview
Divine Mirror AI is a spiritual truth comparison application that reveals how original religious teachings have evolved or been altered throughout history. Built with FastAPI backend, Streamlit frontend, OpenAI GPT-4o, and ChromaDB for semantic search across sacred texts.

## Purpose
Expose the divergence between spiritual originators and modern institutions by comparing authentic ancient texts with modern interpretations, revealing propaganda, fear-based doctrine, and manipulation tactics.

## Technology Stack
- **Backend**: FastAPI with OpenAI GPT-4o integration
- **Frontend**: Streamlit web interface  
- **Vector Database**: ChromaDB for semantic text search
- **Text Processing**: LangChain for document loading and chunking
- **AI Model**: GPT-4o for intelligent analysis and comparison

## Project Architecture
- `backend/`: FastAPI server with document processing and LLM chains
- `frontend/`: Streamlit components for user interface
- `data/texts/`: Organized religious text corpus by tradition/period/type
- `app.py`: Main Streamlit application entry point

## Features
### Three Comparison Modes:
1. **Modern vs Original**: Compare original teachings with current interpretations
2. **Cross-Tradition**: Compare how different religions approach the same concepts  
3. **Timeline Evolution**: Track how teachings changed across historical periods

### Text Organization:
- Directory structure: `[Tradition]/[TimePeriod]/[Type]/filename.txt`
- Metadata extraction from file paths for intelligent filtering
- Support for .txt, .pdf, and .json formats

## Recent Changes
- **Jan 2025**: Initial project setup with full backend and frontend
- **Jan 2025**: Added sample texts from Christianity, Buddhism, Taoism, Islam, Gnosticism, Hermeticism
- **Jan 2025**: Configured OpenAI API key and Streamlit workflow
- **Jan 2025**: Integrated Smart Model Switcher with OpenAI GPT-4o primary and DeepSeek fallback
- **Jan 2025**: Added automatic fallback handling for API quota limits and rate limiting
- **Jan 2025**: Integrated comprehensive Bible Truth Dissections database (76 books including canonical, apocryphal, and pseudepigraphic texts)
- **Jan 2025**: Added intelligent spiritual fallback responses for offline operation
- **Jan 2025**: Integrated JonnyG's comprehensive Yeshua truth analysis documents covering Truth vs Control, Kingdom Within, Love vs Ritual, Religious Hypocrisy, Biblical Manipulations
- **Jan 2025**: Enhanced fallback system with detailed knowledge of Yeshua's authentic teachings versus institutional corruptions
- **Jan 2025**: Added Jesus Life Map images (25 locations from Nazareth to Ascension)

## Current Status
- Streamlit frontend running on port 5000
- Backend API running on port 8000 with smart model switching
- Smart Model Switcher provides detailed responses about Yeshua's teachings, Church manipulations, and biblical truth dissections
- Comprehensive database now includes: 76 Bible Truth Dissection books, JonnyG's analytical frameworks, and Jesus geographical journey maps
- System operates as powerful truth-seeking tool for exposing religious institutional control versus authentic spiritual teachings
- Ready to support YouTube series production on "Unveiling Yeshua: The Truth Behind the Bible"

## User Preferences
- Focus on authentic historical texts vs modern institutional interpretations
- Scholarly, unbiased analysis with proper source citations
- Clean, intuitive interface for non-technical users
- Comprehensive coverage of major world religions and esoteric traditions