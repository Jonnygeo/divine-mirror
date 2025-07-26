#!/usr/bin/env python3
"""
Automatic Sacred Text Import for Divine Mirror AI
Integrates into main application startup for seamless sacred text availability
"""

import os
import zipfile
import requests
from io import BytesIO
import json
from pathlib import Path

def check_sacred_texts_available():
    """Check if sacred texts are already available"""
    required_files = [
        "data/texts",
        "data/metadata/sacred_metadata.json",
        "data/indexes/text_index.json"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            return False
    
    # Check if we have substantial content
    try:
        with open("data/metadata/sacred_metadata.json", 'r') as f:
            metadata = json.load(f)
            if metadata.get("total_documents", 0) < 100:
                return False
    except:
        return False
    
    return True

def download_and_extract_sacred_texts():
    """Download and extract sacred texts if not already available"""
    if check_sacred_texts_available():
        print("✓ Sacred texts already available")
        return True
    
    zip_url = "https://neo-shade.com/assets/divine_mirror_full_sacred_texts.zip"
    target_dir = "data/texts"
    
    print("🔽 Downloading sacred texts database...")
    
    try:
        # Create directories
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs("data/metadata", exist_ok=True)
        os.makedirs("data/indexes", exist_ok=True)
        
        # Download
        response = requests.get(zip_url, timeout=120)
        if response.status_code != 200:
            print(f"❌ Download failed: HTTP {response.status_code}")
            return False
        
        # Extract
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(target_dir)
        
        print("✓ Sacred texts extracted successfully")
        
        # Create index if needed
        if not os.path.exists("data/indexes/text_index.json"):
            print("🔧 Creating text index...")
            from setup_sacred_database import create_local_text_index
            create_local_text_index()
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading sacred texts: {e}")
        return False

def ensure_sacred_texts_ready():
    """Ensure sacred texts are ready for the application"""
    success = download_and_extract_sacred_texts()
    
    if not success:
        print("⚠️  Sacred texts download failed, using local fallback")
        # Create minimal structure for app to function
        os.makedirs("data/texts", exist_ok=True)
        os.makedirs("data/metadata", exist_ok=True)
        
        # Create basic metadata
        basic_metadata = {
            "total_documents": 0,
            "status": "fallback_mode",
            "message": "Sacred texts not available, using fallback responses"
        }
        
        with open("data/metadata/sacred_metadata.json", 'w') as f:
            json.dump(basic_metadata, f, indent=2)
    
    # Update stats after ensuring texts are ready
    try:
        from stats_calculator import save_stats_to_file
        save_stats_to_file()
        print("✓ Stats updated")
    except Exception as e:
        print(f"⚠️  Stats update failed: {e}")
    
    return success

if __name__ == "__main__":
    ensure_sacred_texts_ready()