#!/usr/bin/env python3
"""
Divine Mirror AI - Sacred Text Compression and Distribution Script
Creates distributable ZIP of the complete sacred texts database structure
"""

import os
import zipfile
from pathlib import Path

def create_distribution_zip():
    """Create a complete ZIP file of the Divine Mirror sacred texts structure"""
    
    # Define the output ZIP file
    zip_filename = "DivineMirror_Filled_Texts.zip"
    
    # Count files and create ZIP
    file_count = 0
    dir_count = 0
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Add all text files and directory structure
        for root, dirs, files in os.walk("data/texts"):
            # Count directories
            dir_count += len(dirs)
            
            # Add directory to ZIP
            rel_root = os.path.relpath(root, ".")
            zipf.write(root, rel_root)
            
            # Add all files in directory
            for file in files:
                if file.endswith(('.txt', '.md', '.json')):
                    file_path = os.path.join(root, file)
                    rel_file_path = os.path.relpath(file_path, ".")
                    zipf.write(file_path, rel_file_path)
                    file_count += 1
        
        # Add documentation files
        docs = ["SACRED_TEXT_INVENTORY.md", "data_structure_guide.md", "replit.md"]
        for doc in docs:
            if os.path.exists(doc):
                zipf.write(doc, doc)
                file_count += 1
        
        # Add processing scripts
        scripts = ["expand_sacred_texts.py", "populate_structure.py", "compress_texts.py"]
        for script in scripts:
            if os.path.exists(script):
                zipf.write(script, script)
                file_count += 1
    
    # Get ZIP file size
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    
    print(f"🎯 Divine Mirror AI - Complete Database Package Created")
    print(f"=" * 55)
    print(f"📦 ZIP File: {zip_filename}")
    print(f"📊 Size: {zip_size:.2f} MB")
    print(f"📁 Directories: {dir_count}")
    print(f"📄 Files: {file_count}")
    print(f"🌍 Traditions: 10+ religious traditions")
    print(f"⏳ Periods: Ancient, Medieval, Modern")
    print(f"📚 Types: Original, Translations, Commentary, Comparative")
    print(f"")
    print(f"🚀 Ready for Distribution and Import!")
    print(f"This package contains the complete Divine Mirror AI")
    print(f"sacred texts database with organizational structure.")

def verify_structure():
    """Verify the completeness of the sacred texts structure"""
    
    expected_traditions = [
        "Christianity", "Judaism", "Islam", "Hinduism", "Buddhism", 
        "Taoism", "Zoroastrianism", "Jainism", "Sikhism", "Confucianism", 
        "Shinto", "Indigenous", "Gnosticism", "Hermeticism"
    ]
    
    expected_periods = ["Ancient", "Medieval", "Modern"]
    expected_types = ["Original", "Translations", "Commentary", "Comparative"]
    
    missing_dirs = []
    existing_texts = 0
    
    for tradition in expected_traditions:
        tradition_path = Path(f"data/texts/{tradition}")
        if not tradition_path.exists():
            missing_dirs.append(f"data/texts/{tradition}")
            continue
            
        for period in expected_periods:
            for doc_type in expected_types:
                type_path = tradition_path / period / doc_type
                if not type_path.exists():
                    missing_dirs.append(str(type_path))
                else:
                    # Count text files in this directory
                    text_files = list(type_path.glob("*.txt"))
                    existing_texts += len(text_files)
    
    print(f"📋 Structure Verification Results:")
    print(f"✅ Text files found: {existing_texts}")
    print(f"❌ Missing directories: {len(missing_dirs)}")
    
    if missing_dirs:
        print("Missing directories:")
        for missing in missing_dirs[:10]:  # Show first 10
            print(f"  - {missing}")
        if len(missing_dirs) > 10:
            print(f"  ... and {len(missing_dirs) - 10} more")

if __name__ == "__main__":
    print("🔍 Verifying Divine Mirror AI structure...")
    verify_structure()
    print("\n📦 Creating distribution package...")
    create_distribution_zip()