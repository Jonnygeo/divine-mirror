#!/usr/bin/env python3
"""
Divine Mirror AI - Automatic Content Ingestion System
Converts PDFs, EPUBs, and other formats to text for the sacred texts database
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict

class SacredTextIngester:
    """Automated system for ingesting various document formats into Divine Mirror AI"""
    
    def __init__(self):
        self.base_path = Path("data/texts")
        self.staging_path = Path("staging")
        self.staging_path.mkdir(exist_ok=True)
        
        # Supported file extensions
        self.supported_formats = {
            '.txt': self.process_text,
            '.md': self.process_markdown,
            '.json': self.process_json,
            '.pdf': self.process_pdf,
            '.epub': self.process_epub,
            '.docx': self.process_docx,
            '.html': self.process_html
        }
        
        # Tradition keywords for auto-classification
        self.tradition_keywords = {
            'Christianity': ['jesus', 'christ', 'bible', 'gospel', 'christian', 'church', 'yeshua'],
            'Judaism': ['torah', 'talmud', 'jewish', 'hebrew', 'tanakh', 'mishnah', 'rabbi'],
            'Islam': ['quran', 'koran', 'muslim', 'islamic', 'allah', 'prophet', 'hadith'],
            'Hinduism': ['hindu', 'vedas', 'upanishad', 'gita', 'krishna', 'sanskrit', 'dharma'],
            'Buddhism': ['buddha', 'buddhist', 'dharma', 'sangha', 'sutra', 'zen', 'meditation'],
            'Taoism': ['tao', 'taoist', 'lao', 'zhuang', 'ching', 'wu wei', 'yin yang'],
            'Confucianism': ['confucius', 'analects', 'mencius', 'chinese philosophy', 'virtue'],
            'Sikhism': ['sikh', 'guru', 'granth', 'sahib', 'punjabi', 'khalsa'],
            'Jainism': ['jain', 'mahavira', 'ahimsa', 'non-violence', 'jina'],
            'Zoroastrianism': ['zoroaster', 'avesta', 'ahura', 'mazda', 'persian', 'parsi'],
            'Bahai': ['bahai', "baha'i", 'bahaullah', 'abdul-baha', 'kitab', 'aqdas', 'bab'],
            'Shinto': ['shinto', 'kami', 'kojiki', 'nihon', 'japanese', 'shrine'],
            'Indigenous': ['native', 'indigenous', 'tribal', 'shamanic', 'oral tradition', 'aboriginal'],
            'Gnosticism': ['gnostic', 'nag hammadi', 'sophia', 'demiurge', 'pistis'],
            'Other': ['hermetic', 'hermes', 'trismegistus', 'emerald', 'alchemy', 'esoteric', 'occult', 'mystery']
        }
        
        # Period keywords for auto-classification
        self.period_keywords = {
            'Ancient': ['ancient', 'classical', 'original', 'early', 'primitive', '1st century', '2nd century'],
            'Medieval': ['medieval', 'middle ages', 'scholastic', 'patristic', 'church fathers'],
            'Modern': ['modern', 'contemporary', 'reformation', 'enlightenment', 'recent']
        }
        
        # Type keywords for auto-classification
        self.type_keywords = {
            'Original': ['original', 'source', 'primary', 'authentic', 'canonical'],
            'Translations': ['translation', 'version', 'translated', 'english', 'vernacular'],
            'Commentary': ['commentary', 'analysis', 'interpretation', 'scholarly', 'study'],
            'Comparative': ['comparative', 'comparison', 'cross-tradition', 'inter-religious']
        }
    
    def process_text(self, file_path: Path) -> str:
        """Process plain text files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def process_markdown(self, file_path: Path) -> str:
        """Process markdown files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Remove markdown formatting for pure text
            content = re.sub(r'#{1,6}\s+', '', content)  # Headers
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
            content = re.sub(r'\*(.*?)\*', r'\1', content)  # Italic
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # Links
            return content
    
    def process_json(self, file_path: Path) -> str:
        """Process JSON files containing text data"""
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract text from common JSON structures
            if isinstance(data, dict):
                if 'text' in data:
                    return data['text']
                elif 'content' in data:
                    return data['content']
                elif 'body' in data:
                    return data['body']
                else:
                    # Concatenate all string values
                    return ' '.join(str(v) for v in data.values() if isinstance(v, str))
            
            return str(data)
        except:
            return f"Error processing JSON file: {file_path}"
    
    def process_pdf(self, file_path: Path) -> str:
        """Process PDF files (placeholder - would need PyPDF2 or similar)"""
        return f"PDF processing not implemented yet for: {file_path}\nPlease convert to .txt manually."
    
    def process_epub(self, file_path: Path) -> str:
        """Process EPUB files (placeholder - would need ebooklib)"""
        return f"EPUB processing not implemented yet for: {file_path}\nPlease convert to .txt manually."
    
    def process_docx(self, file_path: Path) -> str:
        """Process DOCX files (placeholder - would need python-docx)"""
        return f"DOCX processing not implemented yet for: {file_path}\nPlease convert to .txt manually."
    
    def process_html(self, file_path: Path) -> str:
        """Process HTML files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Remove HTML tags
            content = re.sub(r'<[^>]+>', '', content)
            # Clean up whitespace
            content = re.sub(r'\s+', ' ', content)
            return content.strip()
    
    def classify_document(self, filename: str, content: str) -> Dict[str, str]:
        """Automatically classify document by tradition, period, and type"""
        filename_lower = filename.lower()
        content_lower = content.lower()[:1000]  # First 1000 chars
        
        # Classify tradition
        tradition_scores = {}
        for tradition, keywords in self.tradition_keywords.items():
            score = sum(1 for keyword in keywords 
                       if keyword in filename_lower or keyword in content_lower)
            if score > 0:
                tradition_scores[tradition] = score
        
        tradition = max(tradition_scores, key=tradition_scores.get) if tradition_scores else 'Christianity'
        
        # Classify period
        period_scores = {}
        for period, keywords in self.period_keywords.items():
            score = sum(1 for keyword in keywords 
                       if keyword in filename_lower or keyword in content_lower)
            if score > 0:
                period_scores[period] = score
        
        period = max(period_scores, key=period_scores.get) if period_scores else 'Modern'
        
        # Classify type
        type_scores = {}
        for doc_type, keywords in self.type_keywords.items():
            score = sum(1 for keyword in keywords 
                       if keyword in filename_lower or keyword in content_lower)
            if score > 0:
                type_scores[doc_type] = score
        
        doc_type = max(type_scores, key=type_scores.get) if type_scores else 'Translations'
        
        return {
            'tradition': tradition,
            'period': period,
            'type': doc_type
        }
    
    def ingest_file(self, source_path: Path, target_filename: str = None) -> bool:
        """Ingest a single file into the sacred texts database"""
        
        # Check if file format is supported
        if source_path.suffix.lower() not in self.supported_formats:
            print(f"❌ Unsupported format: {source_path.suffix}")
            return False
        
        try:
            # Process the file content
            processor = self.supported_formats[source_path.suffix.lower()]
            content = processor(source_path)
            
            if not content.strip():
                print(f"❌ Empty content in: {source_path}")
                return False
            
            # Auto-classify the document
            classification = self.classify_document(source_path.name, content)
            
            # Generate target filename if not provided
            if not target_filename:
                target_filename = source_path.stem + '.txt'
            
            # Create target directory structure
            target_dir = (self.base_path / 
                         classification['tradition'] / 
                         classification['period'] / 
                         classification['type'])
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Write processed content
            target_path = target_dir / target_filename
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Ingested: {source_path.name}")
            print(f"   → {classification['tradition']}/{classification['period']}/{classification['type']}/{target_filename}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {source_path}: {e}")
            return False
    
    def ingest_directory(self, source_dir: Path) -> Dict[str, int]:
        """Ingest all supported files from a directory"""
        
        stats = {'processed': 0, 'failed': 0, 'skipped': 0}
        
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                if file_path.suffix.lower() in self.supported_formats:
                    if self.ingest_file(file_path):
                        stats['processed'] += 1
                    else:
                        stats['failed'] += 1
                else:
                    stats['skipped'] += 1
        
        return stats
    
    def batch_ingest_from_staging(self) -> None:
        """Process all files in the staging directory"""
        
        print(f"🔄 Starting batch ingestion from {self.staging_path}")
        print("=" * 50)
        
        if not self.staging_path.exists() or not any(self.staging_path.iterdir()):
            print("📭 No files found in staging directory")
            print(f"Place files to ingest in: {self.staging_path}")
            return
        
        stats = self.ingest_directory(self.staging_path)
        
        print(f"\n📊 Ingestion Complete:")
        print(f"✅ Processed: {stats['processed']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"⏭️ Skipped: {stats['skipped']}")
        
        # Clean up staging area
        if stats['processed'] > 0:
            print(f"\n🧹 Cleaning staging directory...")
            for file_path in self.staging_path.rglob('*'):
                if file_path.is_file():
                    file_path.unlink()

def main():
    """Main function for testing and demonstration"""
    ingester = SacredTextIngester()
    
    print("🕊️ Divine Mirror AI - Automatic Content Ingestion System")
    print("=" * 55)
    print("📁 Supported formats:", list(ingester.supported_formats.keys()))
    print(f"📂 Staging directory: {ingester.staging_path}")
    print(f"🎯 Target database: {ingester.base_path}")
    print()
    
    # Check for files in staging
    if ingester.staging_path.exists():
        staging_files = list(ingester.staging_path.rglob('*'))
        if staging_files:
            print(f"📋 Found {len(staging_files)} items in staging")
            ingester.batch_ingest_from_staging()
        else:
            print("📭 No files in staging directory")
            print("💡 Usage:")
            print("   1. Place files in the 'staging/' directory")
            print("   2. Run this script to auto-ingest them")
            print("   3. Files will be automatically classified and organized")
    else:
        print("📁 Creating staging directory...")
        ingester.staging_path.mkdir(exist_ok=True)

if __name__ == "__main__":
    main()