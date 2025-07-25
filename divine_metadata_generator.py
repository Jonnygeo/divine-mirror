#!/usr/bin/env python3
"""
Divine Mirror AI - Metadata Generator
Creates JSON metadata for all sacred texts for enhanced search and categorization
"""

import os
import json
from pathlib import Path
from datetime import datetime

def generate_metadata():
    """Generate comprehensive metadata for all texts in the Divine Mirror database"""
    
    base_path = Path("data/texts")
    metadata = {
        "generated": datetime.now().isoformat(),
        "database_version": "1.0",
        "total_files": 0,
        "traditions": {},
        "files": []
    }
    
    tradition_counts = {}
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.txt') and file != 'README.md':
                file_path = Path(root) / file
                relative_path = file_path.relative_to(base_path)
                
                # Parse path components
                path_parts = relative_path.parts
                if len(path_parts) >= 3:
                    tradition = path_parts[0]
                    period = path_parts[1]
                    doc_type = path_parts[2]
                    
                    # Count tradition files
                    if tradition not in tradition_counts:
                        tradition_counts[tradition] = 0
                    tradition_counts[tradition] += 1
                    
                    # Get file stats
                    stat = file_path.stat()
                    file_size = stat.st_size
                    
                    # Count words (approximate)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            word_count = len(content.split())
                            char_count = len(content)
                    except:
                        word_count = 0
                        char_count = 0
                    
                    # Create file metadata
                    file_metadata = {
                        "filename": file,
                        "path": str(relative_path),
                        "tradition": tradition,
                        "period": period,
                        "type": doc_type,
                        "size_bytes": file_size,
                        "word_count": word_count,
                        "char_count": char_count,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    
                    # Add source information based on filename
                    if "KJV" in file or "King James" in file:
                        file_metadata["source"] = "Project Gutenberg - King James Bible"
                        file_metadata["authenticity"] = "high"
                        file_metadata["language"] = "English"
                        file_metadata["year"] = "1611"
                    elif "YLT" in file or "Young" in file:
                        file_metadata["source"] = "Project Gutenberg - Young's Literal Translation"
                        file_metadata["authenticity"] = "high"
                        file_metadata["language"] = "English"
                        file_metadata["year"] = "1898"
                    elif "Dhammapada" in file:
                        file_metadata["source"] = "Sacred-texts.com - Buddhist Canon"
                        file_metadata["authenticity"] = "high"
                        file_metadata["language"] = "English Translation"
                        file_metadata["year"] = "Ancient"
                    elif "Tao" in file:
                        file_metadata["source"] = "Sacred-texts.com - Taoist Canon"
                        file_metadata["authenticity"] = "high"
                        file_metadata["language"] = "English Translation"
                        file_metadata["year"] = "Ancient"
                    elif "Avesta" in file:
                        file_metadata["source"] = "Sacred-texts.com - Zoroastrian Canon"
                        file_metadata["authenticity"] = "high"
                        file_metadata["language"] = "English Translation"
                        file_metadata["year"] = "Ancient"
                    elif "Masoretic" in file:
                        file_metadata["source"] = "Sacred-texts.com - Hebrew Bible"
                        file_metadata["authenticity"] = "high"
                        file_metadata["language"] = "English Translation"
                        file_metadata["year"] = "Ancient"
                    else:
                        file_metadata["source"] = "Divine Mirror Collection"
                        file_metadata["authenticity"] = "verified"
                        file_metadata["language"] = "Various"
                        file_metadata["year"] = "Various"
                    
                    metadata["files"].append(file_metadata)
                    metadata["total_files"] += 1
    
    # Add tradition summaries
    metadata["traditions"] = tradition_counts
    
    # Write metadata file
    with open("divine_mirror_metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Divine Mirror AI - Metadata Generated")
    print(f"=" * 45)
    print(f"📄 Total files: {metadata['total_files']}")
    print(f"🌍 Traditions: {len(tradition_counts)}")
    
    for tradition, count in sorted(tradition_counts.items()):
        print(f"   {tradition}: {count} texts")
    
    print(f"💾 Metadata saved to: divine_mirror_metadata.json")
    print(f"🗄️ Database ready for vector ingestion!")

if __name__ == "__main__":
    generate_metadata()