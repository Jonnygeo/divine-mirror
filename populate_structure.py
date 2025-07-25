#!/usr/bin/env python3
"""
Divine Mirror AI - Directory Structure Population Script
Creates the complete organizational framework for sacred texts analysis
"""

import os
from pathlib import Path

# Define the tradition/period/type structure
TRADITIONS = [
    "Christianity", "Judaism", "Islam", "Hinduism", 
    "Buddhism", "Taoism", "Zoroastrianism"
]

PERIODS = ["Ancient", "Medieval", "Modern"]

TYPES = ["Original", "Translations", "Commentary", "Comparative"]

def create_structure():
    """Create the complete directory structure"""
    base_path = Path("data/texts")
    
    for tradition in TRADITIONS:
        for period in PERIODS:
            for doc_type in TYPES:
                dir_path = base_path / tradition / period / doc_type
                dir_path.mkdir(parents=True, exist_ok=True)
                
                # Create placeholder README in each directory
                readme_path = dir_path / "README.md"
                if not readme_path.exists():
                    with open(readme_path, 'w') as f:
                        f.write(f"# {tradition} - {period} - {doc_type}\n\n")
                        f.write(f"Directory for {doc_type.lower()} texts from the {period.lower()} period of {tradition}.\n\n")
                        f.write("## Purpose\n")
                        if doc_type == "Original":
                            f.write("Contains texts in their original languages and earliest available forms.\n")
                        elif doc_type == "Translations":
                            f.write("Contains translations into various languages and historical periods.\n")
                        elif doc_type == "Commentary":
                            f.write("Contains scholarly analysis and commentary on the texts.\n")
                        elif doc_type == "Comparative":
                            f.write("Contains comparative analysis with other traditions and periods.\n")
    
    print(f"✅ Created complete structure for {len(TRADITIONS)} traditions")
    print(f"📁 Total directories: {len(TRADITIONS) * len(PERIODS) * len(TYPES)}")
    
    # Count existing text files
    text_count = len(list(base_path.rglob("*.txt")))
    print(f"📄 Current text files: {text_count}")

if __name__ == "__main__":
    create_structure()
