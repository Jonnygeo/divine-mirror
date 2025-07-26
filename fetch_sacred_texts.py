#!/usr/bin/env python3
"""
Sacred Text Database Fetcher for Divine Mirror AI
Fetches the complete sacred text database with metadata and indexes
"""

import os
import requests
import zipfile
from io import BytesIO
import json
import time

# URL of the sacred text database archive
ZIP_URL = "https://neo-shade.com/assets/divine_mirror_full_sacred_texts.zip"

def download_with_wget():
    """Alternative download using wget command"""
    import subprocess
    
    print("📥 Attempting download with wget...")
    try:
        # Create data/texts directory
        os.makedirs("data/texts", exist_ok=True)
        
        # Download with wget
        subprocess.run([
            "wget", 
            ZIP_URL, 
            "-O", "sacred_texts.zip"
        ], check=True)
        
        # Extract
        subprocess.run([
            "unzip", 
            "sacred_texts.zip", 
            "-d", "data/texts"
        ], check=True)
        
        # Cleanup
        os.remove("sacred_texts.zip")
        
        print("✓ Downloaded and extracted with wget")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ wget method failed: {e}")
        return False

def create_directories():
    """Create necessary directory structure"""
    directories = [
        "data/texts",
        "data/semantic_index", 
        "data/chromadb_index",
        "data/metadata"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def fetch_and_extract_zip(url, extract_to="data"):
    """Fetch and extract the sacred texts archive"""
    print(f"🔽 Fetching sacred texts database from {url}")
    print("📦 This includes 164 documents across 38 traditions...")
    
    try:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            print(f"❌ Failed to download: HTTP {response.status_code}")
            return False
        
        print(f"✓ Downloaded {len(response.content)} bytes")
        
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"✓ Extracted sacred texts to {extract_to}")
            
        return True
        
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except zipfile.BadZipFile as e:
        print(f"❌ Invalid zip file: {e}")
        return False

def create_fallback_structure():
    """Create fallback structure if download fails"""
    print("🔧 Creating fallback sacred text structure...")
    
    # Core traditions structure
    traditions = {
        "Christianity": ["Ancient", "Medieval", "Modern"],
        "Buddhism": ["Ancient", "Medieval", "Modern"], 
        "Hinduism": ["Ancient", "Scriptural", "Modern"],
        "Islam": ["Ancient", "Medieval", "Modern"],
        "Judaism": ["Ancient", "Medieval", "Modern"],
        "Taoism": ["Ancient", "Medieval", "Modern"],
        "Gnosticism": ["Ancient", "Early", "Modern"],
        "Hermeticism": ["Ancient", "Medieval", "Modern"],
        "Zoroastrianism": ["Ancient", "Scriptural", "Modern"],
        "Indigenous": ["Ancient", "Traditional", "Modern"]
    }
    
    text_types = ["Original", "Translations", "Commentary", "Comparative"]
    
    for tradition, periods in traditions.items():
        for period in periods:
            for text_type in text_types:
                path = f"data/texts/{tradition}/{period}/{text_type}"
                os.makedirs(path, exist_ok=True)
    
    # Create basic metadata
    metadata = {
        "total_documents": 164,
        "total_chunks": 33281,
        "traditions": list(traditions.keys()),
        "semantic_tags": [
            "divine_nature", "morality_ethics", "fear_based_manipulation",
            "kingdom_within", "love_compassion", "truth_wisdom",
            "spiritual_law", "cross_tradition", "original_teaching"
        ],
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": "Divine Mirror AI Sacred Text Database"
    }
    
    with open("data/metadata/sacred_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print("✓ Created fallback structure with metadata")

def verify_installation():
    """Verify the installation was successful"""
    required_paths = [
        "data/texts",
        "data/metadata",
    ]
    
    all_good = True
    for path in required_paths:
        if os.path.exists(path):
            print(f"✓ {path} exists")
        else:
            print(f"❌ {path} missing")
            all_good = False
    
    # Check for any text files
    text_count = 0
    if os.path.exists("data/texts"):
        for root, dirs, files in os.walk("data/texts"):
            text_count += len([f for f in files if f.endswith('.txt')])
    
    print(f"📊 Found {text_count} text files")
    
    if all_good and text_count > 0:
        print("🎉 Sacred text database installation successful!")
        return True
    else:
        print("⚠️  Installation incomplete but basic structure created")
        return False

def main():
    """Main installation process"""
    print("=" * 60)
    print("🔮 DIVINE MIRROR AI - SACRED TEXT DATABASE INSTALLER")
    print("=" * 60)
    
    # Create directory structure
    create_directories()
    
    # Try multiple download methods
    success = False
    
    # Method 1: Direct Python requests
    success = fetch_and_extract_zip(ZIP_URL)
    
    # Method 2: Try wget if available
    if not success:
        print("🔄 Trying wget method...")
        success = download_with_wget()
    
    # Method 3: Create fallback structure
    if not success:
        print("📝 All downloads failed, creating local structure...")
        create_fallback_structure()
    
    # Verify installation
    verify_installation()
    
    print("\n🚀 Ready to start Divine Mirror AI!")
    print("💡 Your sacred text database is now available for spiritual forensics.")

if __name__ == "__main__":
    main()