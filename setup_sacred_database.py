#!/usr/bin/env python3
"""
Sacred Database Setup for Divine Mirror AI
Initializes the local text index and metadata system
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime

def create_local_text_index():
    """Create a local text index for offline search"""
    print("🔍 Creating local text index...")
    
    text_index = {}
    chunk_id = 0
    
    # Search for all text files
    text_files = glob.glob("data/texts/**/*.txt", recursive=True)
    
    for file_path in text_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata from path
            path_parts = Path(file_path).parts
            if len(path_parts) >= 5:  # data/texts/Tradition/Period/Type/file.txt
                tradition = path_parts[2]
                period = path_parts[3] 
                text_type = path_parts[4]
                filename = path_parts[-1]
                
                # Split into chunks (roughly 500 characters)
                chunks = [content[i:i+500] for i in range(0, len(content), 400)]
                
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) > 50:  # Only meaningful chunks
                        text_index[chunk_id] = {
                            "text": chunk.strip(),
                            "source_file": file_path,
                            "tradition": tradition,
                            "period": period,
                            "text_type": text_type,
                            "title": filename.replace('.txt', ''),
                            "chunk_index": i,
                            "keywords": extract_keywords(chunk)
                        }
                        chunk_id += 1
        
        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")
    
    # Save index
    os.makedirs("data/indexes", exist_ok=True)
    with open("data/indexes/text_index.json", 'w') as f:
        json.dump(text_index, f, indent=2)
    
    print(f"✓ Created index with {len(text_index)} text chunks")
    return len(text_index)

def extract_keywords(text):
    """Extract keywords from text for search"""
    # Basic keyword extraction
    words = text.lower().split()
    
    # Spiritual/religious keywords
    spiritual_keywords = [
        'god', 'divine', 'spirit', 'soul', 'kingdom', 'heaven', 'love',
        'forgiveness', 'truth', 'wisdom', 'compassion', 'peace', 'faith',
        'prayer', 'meditation', 'enlightenment', 'salvation', 'grace',
        'jesus', 'christ', 'buddha', 'allah', 'tao', 'brahman', 'atman'
    ]
    
    found_keywords = []
    for word in words:
        clean_word = word.strip('.,!?";:()[]{}')
        if clean_word in spiritual_keywords:
            found_keywords.append(clean_word)
    
    return list(set(found_keywords))  # Remove duplicates

def create_tradition_summary():
    """Create summary of available traditions"""
    print("📊 Creating tradition summary...")
    
    traditions = {}
    
    if os.path.exists("data/texts"):
        for tradition_dir in os.listdir("data/texts"):
            tradition_path = f"data/texts/{tradition_dir}"
            if os.path.isdir(tradition_path):
                
                # Count files in this tradition
                file_count = len(glob.glob(f"{tradition_path}/**/*.txt", recursive=True))
                
                # Get periods
                periods = []
                if os.path.exists(tradition_path):
                    periods = [d for d in os.listdir(tradition_path) if os.path.isdir(f"{tradition_path}/{d}")]
                
                traditions[tradition_dir] = {
                    "file_count": file_count,
                    "periods": periods,
                    "description": get_tradition_description(tradition_dir)
                }
    
    # Save summary
    with open("data/metadata/tradition_summary.json", 'w') as f:
        json.dump(traditions, f, indent=2)
    
    print(f"✓ Cataloged {len(traditions)} traditions")
    return traditions

def get_tradition_description(tradition):
    """Get description for tradition"""
    descriptions = {
        "Christianity": "Teachings of Jesus/Yeshua, Biblical texts, and Christian theology",
        "Buddhism": "Buddha's teachings, sutras, and Buddhist philosophy", 
        "Hinduism": "Vedas, Upanishads, Bhagavad Gita, and Hindu scriptures",
        "Islam": "Quran, Hadith, and Islamic teachings",
        "Judaism": "Torah, Talmud, and Jewish sacred texts",
        "Taoism": "Tao Te Ching, I Ching, and Taoist philosophy",
        "Gnosticism": "Gnostic gospels and early Christian mysticism",
        "Hermeticism": "Hermetic texts and ancient wisdom traditions",
        "Zoroastrianism": "Avesta and Zoroastrian teachings",
        "Indigenous": "Native wisdom traditions and spiritual teachings"
    }
    return descriptions.get(tradition, "Sacred texts and spiritual teachings")

def create_search_config():
    """Create search configuration"""
    search_config = {
        "search_methods": ["keyword", "semantic", "cross_tradition"],
        "supported_languages": ["english", "hebrew", "greek", "arabic", "sanskrit"],
        "search_fields": ["text", "title", "tradition", "period", "keywords"],
        "max_results": 10,
        "chunk_overlap": 50,
        "min_chunk_size": 50,
        "spiritual_themes": [
            "divine_nature", "kingdom_within", "love_compassion", 
            "truth_wisdom", "forgiveness", "salvation", "enlightenment",
            "prayer_meditation", "spiritual_law", "cross_tradition"
        ]
    }
    
    with open("data/metadata/search_config.json", 'w') as f:
        json.dump(search_config, f, indent=2)
    
    print("✓ Created search configuration")

def main():
    """Main setup process"""
    print("=" * 50)
    print("🔧 DIVINE MIRROR AI - DATABASE SETUP")
    print("=" * 50)
    
    # Create metadata directory
    os.makedirs("data/metadata", exist_ok=True)
    
    # Create text index
    chunk_count = create_local_text_index()
    
    # Create tradition summary
    traditions = create_tradition_summary()
    
    # Create search config
    create_search_config()
    
    # Create overall status
    status = {
        "setup_complete": True,
        "setup_date": datetime.now().isoformat(),
        "total_chunks": chunk_count,
        "total_traditions": len(traditions),
        "index_file": "data/indexes/text_index.json",
        "version": "1.0.0"
    }
    
    with open("data/metadata/setup_status.json", 'w') as f:
        json.dump(status, f, indent=2)
    
    print("\n🎉 Database setup complete!")
    print(f"📊 {chunk_count} text chunks indexed")
    print(f"🌍 {len(traditions)} traditions available")
    print("🔮 Divine Mirror AI ready for spiritual forensics!")

if __name__ == "__main__":
    main()