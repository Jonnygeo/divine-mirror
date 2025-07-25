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
- **Jan 2025**: Created comprehensive Bible Dissection Project framework with systematic methodology for exposing manipulations
- **Jan 2025**: Developed video script templates for YouTube series with hook formulas, evidence presentation, and truth revelation structures
- **Jan 2025**: Fixed empty response issue - enhanced fallback system now properly triggers when AI models return empty content
- **Jan 2025**: MAJOR UPGRADE: Integrated complete sacred text library (115 documents, 252 semantic chunks) including original language texts, multiple translations, non-canonical works, and multi-religious scriptures

## Current Status
- Streamlit frontend running on port 5000
- Backend API running on port 8000 with smart model switching  
- Smart Model Switcher provides detailed responses about Yeshua's teachings, Church manipulations, and biblical truth dissections
- ENHANCED DATABASE: 115 documents including complete Bible collection, original language texts (Septuagint, Textus Receptus, Dead Sea Scrolls), multiple translations (KJV, NIV, YLT), non-canonical works (Nag Hammadi, Gospel of Thomas/Mary/Philip/Judas, Book of Enoch), and multi-religious scriptures (Quran, Pali Canon, Vedas, Upanishads, Tao Te Ching, Avesta)
- Comprehensive truth analysis framework with 252 semantic chunks for cross-referencing and comparative analysis
- Complete YouTube series structure with 10 episode outlines exposing Truth vs Control, Kingdom Within, Love vs Ritual, Religious Hypocrisy, Biblical Manipulations
- System operates as comprehensive truth-seeking platform with vast authentic source material for exposing institutional manipulations

## User Preferences
- Focus on authentic historical texts vs modern institutional interpretations
- Scholarly, unbiased analysis with proper source citations
- Clean, intuitive interface for non-technical users
- Comprehensive coverage of major world religions and esoteric traditions