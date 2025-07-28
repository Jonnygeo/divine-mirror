# 🔮 Divine Mirror AI

**A semantic search and spiritual comparison engine using vectorized sacred texts**

---

## 🔍 What It Does

Divine Mirror AI allows users to ask deep, spiritually-driven questions like:

- “What did Yeshua actually teach about forgiveness?”
- “How does the Tao compare to the Gospels on peace?”
- “What do different traditions say about the soul's journey?”

The system uses a vector database built from **131 sacred texts** including:

- The Bible (multiple versions, including red-letter extractions of Yeshua's words)  
- The Quran, Tao Te Ching, Vedas, Dead Sea Scrolls, Apocrypha, Nag Hammadi  
- Original-language sacred texts (Greek, Hebrew, Sanskrit, Arabic)  
- Non-canonical spiritual texts (Gospel of Mary, Book of Enoch, etc.)

---

## 📦 Database Structure

```

data/texts/\[Tradition]/\[Period]/\[Type]/
├── Original/      # Source language texts
├── Translations/  # Standard + literal versions
├── Commentary/    # Scholarly reflections
└── Comparative/   # Inter-tradition references

````

**Current Database**: 131 documents (9.85 MB uncompressed, 3.26 MB compressed)

---

## 🧠 Technologies Used

- **Backend**: Python with FastAPI  
- **Vector Search**: ChromaDB for semantic similarity  
- **AI Integration**: OpenAI GPT-4o with DeepSeek fallback  
- **Text Processing**: LangChain for document loading and chunking  
- **Frontend**: Streamlit with modern glassmorphism UI  
- **Offline Fallback**: Built-in spiritual truth responses

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Jonnygeo/divine-mirror.git
cd divine-mirror-ai
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

```bash
cp .env.example .env
# Add your OPENAI_API_KEY inside .env
```

### 4. Load Sacred Texts

```bash
# Option 1: Download additional texts
python3 divine_mirror_loader.py

# Option 2: Extract from archive
unzip DivineMirror_Filled_Texts.zip
```

### 5. Run the Application

```bash
# Start backend API
python -m backend.api

# Start frontend (in another terminal)
streamlit run app.py --server.port 5000
```

---

## 🎯 Features

### 🔁 Comparison Modes

1. **Modern vs Original** – Compare original teachings vs modern translations
2. **Cross-Tradition** – See how different faiths speak on shared concepts
3. **Timeline Evolution** – Trace how doctrine shifted over time

### 💡 Smart AI System

* **Primary**: OpenAI GPT-4o
* **Fallback**: DeepSeek for token usage
* **Offline Mode**: Spiritual truth engine for low-connectivity usage

### 🖥 Interface Highlights

* Modern glassmorphism theme
* Instant search with Enter key
* Real-time filtering by tradition & date
* Expandable references with citations

---

## 📚 Sacred Text Collection

### ✝️ Christianity (105 texts)

* Bible (KJV, YLT, NIV)
* Greek Septuagint, Dead Sea Scrolls
* Gnostic texts: Thomas, Mary, Judas, Philip
* Red-letter teachings of Yeshua
* 76-book "Bible Dissection" analysis

### 🌍 Multi-Faith Texts

* **Islam**: Quran in Arabic + translations
* **Hinduism**: Vedas, Upanishads
* **Taoism**: Tao Te Ching
* **Buddhism**: Pali Canon, Dhammapada
* **Zoroastrianism**: Avesta
* **Judaism**: Torah, Talmud references
* **Gnosticism**: Hermetic and apocryphal texts

---

## ⚠️ Legal & Ethical

### ✅ Educational Use Only:

* Free spiritual research
* Comparative theology study
* Personal growth and exploration

### ❌ Not for:

* Monetization
* Religious dogma enforcement
* Commercial sale or distribution

**Core Philosophy**: Spiritual discernment through free inquiry and respect for source integrity.

---

## 🔧 Development

### 🔍 Project Structure

```
├── backend/               # FastAPI endpoints and LLM chains
├── frontend/              # Streamlit app
├── data/texts/            # Sacred texts and subfolders
├── app.py                 # Main entry for UI
├── divine_mirror_loader.py # Text ingestion and download
└── compress_texts.py      # Optimization script
```

### Key Components:

* `backend/api.py` – REST API logic
* `backend/llm_chain.py` – AI response logic
* `backend/embedding_store.py` – ChromaDB interface
* `frontend/components.py` – UI widgets

---

## 📊 Stats

* 131 sacred texts
* 13,107 semantic chunks
* 99,968 lines of KJV-only source
* 66.9% compression ratio
* 10 religions represented

---

## 🎥 Content Creation

Launching the **YouTube series**:
**“Unveiling Yeshua: The Truth Behind the Bible”**

* 10-episode blueprint
* Video scripting templates
* Truth frameworks and hooks
* Designed for educational platforms (YT, Rumble, TikTok)

---

## 🚀 Deployment Options

* ✅ Replit ready
* ✅ Docker container included
* ✅ Run locally
* ✅ GitHub Actions for backend/frontend workflows

---

## 📁 Git Hygiene

See `.gitignore` documentation: [Gitignore Info](./gitignore.md)

**Key exclusions**:

* `.env`, `.DS_Store`, `*.log`, `*.json`, `.pyc`, `__pycache__/`
* `divine_*.json`, `data/indexes/text_index.json`

---

**✨ Divine Mirror AI: Revealing spiritual truth through authentic ancient wisdom**
*Built with reverence for truth. Powered by ethical AI.*


