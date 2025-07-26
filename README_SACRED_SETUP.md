# Divine Mirror AI - Sacred Text Database Setup

## 🚀 Quick Setup Instructions

### Method 1: Automated Python Setup (Recommended)
```bash
python fetch_sacred_texts.py
python setup_sacred_database.py
```

### Method 2: Direct Download (Replit Shell)
```bash
mkdir -p data/texts
wget https://neo-shade.com/assets/divine_mirror_full_sacred_texts.zip -O sacred_texts.zip
unzip sacred_texts.zip -d data/texts
rm sacred_texts.zip
python setup_sacred_database.py
```

### Method 3: Auto-Import Integration
The app now automatically checks for sacred texts on startup and downloads them if missing:

```python
# Already integrated in app.py
from auto_sacred_import import ensure_sacred_texts_ready
ensure_sacred_texts_ready()
```

## 📊 What You Get

- **164+ Sacred Documents**: Complete texts across 17+ traditions
- **64,998 Text Chunks**: Searchable offline index for instant access
- **17 Traditions**: Christianity, Buddhism, Hinduism, Islam, Judaism, Taoism, etc.
- **Offline Operation**: Works without OpenAI API for true independence
- **Structured Metadata**: Rich source information for every text

## 🗂️ Directory Structure
```
data/
├── texts/                    # Raw sacred text files
│   ├── Christianity/
│   ├── Buddhism/
│   ├── Hinduism/
│   └── [14 more traditions]/
├── indexes/
│   └── text_index.json      # 64,998 searchable chunks
├── metadata/
│   ├── sacred_metadata.json # Database statistics
│   ├── tradition_summary.json
│   └── search_config.json
└── chromadb/                # Vector database (when OpenAI available)
```

## 🔍 Search Capabilities

### Keyword Search
```python
from offline_search_engine import OfflineSearchEngine
engine = OfflineSearchEngine()
results = engine.search_by_keywords("kingdom within", limit=5)
```

### Spiritual Theme Search
```python
results = engine.search_spiritual_themes("divine_nature")
```

### Cross-Tradition Analysis
```python
cross_results = engine.get_cross_tradition_insights("love")
```

## 📈 Status Check
```python
# Check if database is ready
from auto_sacred_import import check_sacred_texts_available
if check_sacred_texts_available():
    print("✓ Sacred texts database ready")
```

## 🎯 Integration Points

1. **Streamlit App**: Main interface with enhanced source citations
2. **Voice Interface**: Speech-to-text spiritual queries
3. **Backend API**: FastAPI with offline fallback support
4. **Offline Engine**: 64,998 chunks searchable without external APIs

## 🔧 Troubleshooting

### If Download Fails:
1. Check internet connection
2. Try manual wget method
3. App will create fallback structure automatically

### If Search Returns No Results:
1. Verify `data/indexes/text_index.json` exists
2. Run `python setup_sacred_database.py` to rebuild index
3. Check available traditions with `engine.get_tradition_stats()`

### Verify Installation:
```bash
python -c "from offline_search_engine import OfflineSearchEngine; engine = OfflineSearchEngine(); print(f'Loaded {len(engine.text_index)} chunks')"
```

## 📚 Example Usage

```python
# Search for specific teaching
results = engine.search_by_keywords("love your enemies")

# Get results from specific tradition  
christian_results = engine.search_by_tradition("kingdom", "Christianity")

# Search spiritual themes across traditions
universal_love = engine.search_spiritual_themes("love_compassion")

# Cross-tradition comparison
insights = engine.get_cross_tradition_insights("salvation")
```

---

**Divine Mirror AI**: Authentic spiritual forensics with 64,998 sacred text chunks across 17 traditions. Truth doesn't need to be sold — it just needs to be found.