# 🔮 Divine Mirror AI

**A semantic search and spiritual comparison engine using vectorized sacred texts**

## 🔍 What It Does

Divine Mirror AI allows users to ask deep, spiritually-driven questions like:
- "What did Yeshua actually teach about forgiveness?"
- "How does the Tao compare to the Gospels on peace?"
- "What do different traditions say about the soul's journey?"

The system uses a vector database built from **131 sacred texts** including:
- The Bible (multiple versions, including red-letter extractions of Yeshua's words)
- The Quran, Tao Te Ching, Vedas, Dead Sea Scrolls, Apocrypha, Nag Hammadi
- Original-language sacred texts (Greek, Hebrew, Sanskrit, Arabic)
- Non-canonical spiritual texts (Gospel of Mary, Book of Enoch, etc.)

## 📦 Database Structure

```
data/texts/[Tradition]/[Period]/[Type]/
├── Original/      # Source language texts
├── Translations/  # Standard + literal versions  
├── Commentary/    # Scholarly reflections
└── Comparative/   # Inter-tradition references
```

**Current Database**: 131 documents (9.85 MB uncompressed, 3.26 MB compressed)

## 🧠 Technologies Used

- **Backend**: Python with FastAPI
- **Vector Search**: ChromaDB for semantic similarity
- **AI Integration**: OpenAI GPT-4o with DeepSeek fallback
- **Text Processing**: LangChain for document loading and chunking
- **Frontend**: Streamlit with modern glassmorphism UI
- **Smart Fallback**: Built-in spiritual truth responses for offline operation

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo>
cd divine-mirror-ai
```

### 2. Install Dependencies
```bash
# Python dependencies are managed via pyproject.toml
# Install automatically via Replit or use:
pip install -r requirements.txt
```

### 3. Environment Setup
```bash
# Copy and configure environment
cp .env.example .env
# Add your OPENAI_API_KEY
```

### 4. Load Sacred Texts
```bash
# Download additional texts (optional)
python3 divine_mirror_loader.py

# Or extract from provided archive
unzip DivineMirror_Filled_Texts.zip
```

### 5. Run the Application
```bash
# Start backend API
python -m backend.api

# Start frontend (in another terminal)
streamlit run app.py --server.port 5000
```

## 🎯 Features

### Three Comparison Modes:
1. **Modern vs Original** - Compare original teachings with current interpretations
2. **Cross-Tradition** - Compare how different religions approach concepts
3. **Timeline Evolution** - Track how teachings changed across history

### Smart AI System:
- **Primary**: OpenAI GPT-4o for intelligent analysis
- **Fallback**: DeepSeek integration for quota management
- **Offline**: Built-in spiritual knowledge for emergency responses

### Advanced Interface:
- Modern glassmorphism design
- Enter key submission
- Real-time tradition and period filtering
- Source citations with white text visibility
- Expandable documentation sections

## 📚 Sacred Text Collection

### Christianity (105 texts)
- Complete Bible versions (KJV, YLT, NIV)
- Original language texts (Septuagint, Textus Receptus, Dead Sea Scrolls)
- Non-canonical works (Nag Hammadi, Gospel of Thomas/Mary/Philip/Judas)
- Bible Truth Dissections (76 books of analysis)

### Multi-Religious Scriptures
- **Islam**: Quran (Arabic + multiple translations)
- **Buddhism**: Pali Canon, Dhammapada
- **Hinduism**: Vedas, Upanishads
- **Taoism**: Tao Te Ching, classical texts
- **Zoroastrianism**: Avesta
- **Judaism**: Torah teachings
- **Gnosticism**: Gospel of Thomas, hermetic texts

## ⚠️ Legal & Ethical

**Educational Tool**: This app is designed for:
- Free-use, non-commercial educational research
- Spiritual curiosity and truth-seeking
- Ethical AI usage guided by transparency

**Not for**:
- Monetization or financial use
- Making theological claims of authority
- Commercial distribution

**Philosophy**: Truth-seeking through comparative analysis, guided by free speech principles and scholarly inquiry.

## 🔧 Development

### Project Structure
```
├── backend/           # FastAPI server and AI logic
├── frontend/          # Streamlit components  
├── data/texts/        # Sacred text corpus
├── app.py            # Main Streamlit application
├── compress_texts.py  # Database compression utility
└── divine_mirror_loader.py  # Text download utility
```

### Key Components
- `backend/api.py` - FastAPI server with endpoints
- `backend/llm_chain.py` - AI analysis chains
- `backend/smart_response.py` - Smart model switching
- `backend/embedding_store.py` - Vector database management
- `frontend/components.py` - UI components

## 📊 Stats

- **131 sacred texts** across 10 religious traditions
- **13,107 semantic chunks** for comprehensive search
- **99,968 lines** of authentic biblical text (KJV alone)
- **252+ semantic chunks** for cross-referencing
- **66.9% compression ratio** for efficient distribution

## 🎥 Content Creation

Ready for YouTube series "Unveiling Yeshua: The Truth Behind the Bible":
- 10 episode outlines prepared
- Video script templates with hook formulas
- Evidence presentation structures
- Truth revelation methodologies

## 🚀 Deployment

**Replit Ready**: Configured for easy deployment on Replit platform
**Workflows**: Automated backend and frontend management
**Docker**: Containerization support available
**Local**: Full local development environment

---
## 📁 Git Hygiene

See full `.gitignore` documentation here: [Gitignore Info](./gitignore.md)

Why it matters:
- Keeps sacred text files clean and safe
- Blocks massive JSON and `.env` secrets
- Ensures smooth deployment without bloat

**Divine Mirror AI: Revealing spiritual truth through authentic ancient wisdom** ✨

*Built with reverence for truth, powered by cutting-edge AI, guided by ethical principles*
