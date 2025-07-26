#!/usr/bin/env python3
"""
Utility functions for Divine Mirror AI
Includes the homepage stats function as specified by user requirements
"""

from pathlib import Path
import json
import os
import glob

def get_homepage_stats():
    """
    Get homepage stats exactly as specified by user requirements
    Returns stats for Sacred Texts, Analyzed Documents, Traditions, Semantic Tags, AI Phases
    """
    # Use base path for sacred texts
    base_path = Path("data/texts")
    
    # Count sacred texts (.txt files)
    sacred_texts_count = len(list(base_path.glob("**/*.txt"))) if base_path.exists() else 0
    
    # Count analyzed documents (chunk and meta files)
    analyzed_docs_count = 0
    analyzed_docs_count += len(list(Path("data").glob("**/*.chunk.json")))
    analyzed_docs_count += len(list(Path("data").glob("**/*.meta.json")))
    
    # If no chunk/meta files, use text index as analyzed documents count
    if analyzed_docs_count == 0:
        try:
            index_path = "data/indexes/text_index.json"
            if os.path.exists(index_path):
                with open(index_path, 'r') as f:
                    text_index = json.load(f)
                analyzed_docs_count = len(text_index)
        except:
            analyzed_docs_count = sacred_texts_count
    
    # Extract traditions and tags from metadata files
    traditions = set()
    tags = set()
    
    for meta_file in Path("data").glob("**/*.meta.json"):
        try:
            with open(meta_file, "r") as f:
                meta = json.load(f)
                traditions.add(meta.get("tradition", "Unknown"))
                tags.update(meta.get("tags", []))
        except:
            continue
    
    # If no metadata files, extract from directory structure
    if not traditions and base_path.exists():
        for tradition_dir in base_path.iterdir():
            if tradition_dir.is_dir():
                traditions.add(tradition_dir.name)
    
    # Load additional tags from text index keywords
    try:
        index_path = "data/indexes/text_index.json"
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                text_index = json.load(f)
            for chunk_data in text_index.values():
                keywords = chunk_data.get('keywords', [])
                tags.update(keywords)
    except:
        pass
    
    # Default tags if none found
    if not tags:
        tags = {
            "divine_nature", "morality_ethics", "kingdom_within", 
            "love_compassion", "truth_wisdom", "spiritual_law"
        }
    
    return {
        "sacred_texts": sacred_texts_count,
        "analyzed_documents": analyzed_docs_count,
        "traditions": len(traditions),
        "semantic_tags": len(tags),
        "ai_phases": 9  # Fixed number of completed AI phases
    }

# Backward compatibility - import the main stats calculator
try:
    from stats_calculator import calculate_database_stats, get_display_stats
except ImportError:
    def calculate_database_stats():
        """Fallback database stats calculation"""
        stats = get_homepage_stats()
        return {
            "sacred_texts": stats["sacred_texts"],
            "total_documents": stats["sacred_texts"],
            "analyzed_documents": stats["analyzed_documents"],
            "traditions": stats["traditions"],
            "semantic_tags": stats["semantic_tags"],
            "ai_phases": stats["ai_phases"]
        }
    
    def get_display_stats():
        """Fallback display stats"""
        stats = get_homepage_stats()
        return {
            "Sacred Texts": f"{stats['sacred_texts']:,}",
            "Analyzed Documents": f"{stats['analyzed_documents']:,}",
            "Traditions": f"{stats['traditions']}",
            "Semantic Tags": f"{stats['semantic_tags']}+",
            "AI Phases": f"{stats['ai_phases']} Complete"
        }

if __name__ == "__main__":
    stats = get_homepage_stats()
    print("📊 Homepage Stats:")
    print(f"Sacred Texts: {stats['sacred_texts']}")
    print(f"Analyzed Documents: {stats['analyzed_documents']}")
    print(f"Traditions: {stats['traditions']}")
    print(f"Semantic Tags: {stats['semantic_tags']}")
    print(f"AI Phases: {stats['ai_phases']}")