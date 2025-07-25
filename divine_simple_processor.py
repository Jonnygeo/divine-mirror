#!/usr/bin/env python3
"""
Divine Mirror AI - Simple Text Processor (No External Dependencies)
Creates a searchable text index without embeddings when API quota is exceeded
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
import time

class SimpleTextIndex:
    """Simple text-based search index for sacred texts"""
    
    def __init__(self):
        self.documents = []
        self.word_index = defaultdict(set)
        self.metadata_index = {}
        
    def add_document(self, doc_id, text, metadata):
        """Add a document to the index"""
        self.documents.append({
            'id': doc_id,
            'text': text,
            'metadata': metadata
        })
        
        # Create word index for fast searching
        words = self.extract_words(text)
        for word in words:
            self.word_index[word.lower()].add(doc_id)
        
        self.metadata_index[doc_id] = metadata
    
    def extract_words(self, text):
        """Extract meaningful words from text"""
        # Remove punctuation and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'but', 'for', 'are', 'with', 'his', 'they', 'this', 
            'have', 'from', 'one', 'had', 'were', 'been', 'their', 'said',
            'each', 'which', 'them', 'than', 'many', 'some', 'what', 'would',
            'about', 'into', 'after', 'before', 'also', 'when', 'where', 'who',
            'will', 'more', 'can', 'has', 'may', 'all', 'any', 'could', 'our'
        }
        
        return [word for word in words if word not in stop_words]
    
    def search(self, query, max_results=5):
        """Search for documents matching the query"""
        query_words = self.extract_words(query)
        if not query_words:
            return []
        
        # Find documents containing query words
        doc_scores = defaultdict(int)
        
        for word in query_words:
            if word in self.word_index:
                for doc_id in self.word_index[word]:
                    doc_scores[doc_id] += 1
        
        # Sort by relevance score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top results
        results = []
        for doc_id, score in sorted_docs[:max_results]:
            doc = next(d for d in self.documents if d['id'] == doc_id)
            results.append({
                'document': doc['text'],
                'metadata': doc['metadata'],
                'score': score
            })
        
        return results
    
    def get_statistics(self):
        """Get index statistics"""
        traditions = defaultdict(int)
        for doc in self.documents:
            tradition = doc['metadata'].get('tradition', 'Unknown')
            traditions[tradition] += 1
        
        return {
            'total_documents': len(self.documents),
            'total_words': len(self.word_index),
            'traditions': dict(traditions)
        }

class DivineSimpleProcessor:
    """Simple processor for sacred texts without embeddings"""
    
    def __init__(self):
        self.index = SimpleTextIndex()
        self.processed_count = 0
        self.chunk_count = 0
        
    def chunk_text(self, text, chunk_size=1000):
        """Split text into chunks by word count"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)
        
        return chunks
    
    def extract_metadata(self, filepath):
        """Extract metadata from file path"""
        path_parts = Path(filepath).parts
        
        if len(path_parts) >= 5:
            tradition = path_parts[2]
            period = path_parts[3]
            text_type = path_parts[4]
        else:
            tradition = "Unknown"
            period = "Unknown"
            text_type = "Unknown"
        
        filename = Path(filepath).stem
        
        return {
            "tradition": tradition,
            "period": period,
            "type": text_type,
            "title": filename,
            "source_path": str(filepath),
            "filename": Path(filepath).name
        }
    
    def process_file(self, filepath):
        """Process a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
            
            if not content or len(content) < 50:
                return 0
            
            metadata = self.extract_metadata(filepath)
            chunks = self.chunk_text(content)
            
            chunks_added = 0
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) < 20:
                    continue
                
                doc_id = f"{metadata['tradition']}_{metadata['title']}_{i}"
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_id'] = i
                
                self.index.add_document(doc_id, chunk, chunk_metadata)
                chunks_added += 1
                self.chunk_count += 1
            
            self.processed_count += 1
            print(f"✅ {Path(filepath).name}: {chunks_added} chunks")
            return chunks_added
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return 0
    
    def process_all_texts(self, base_dir="data/texts"):
        """Process all text files"""
        print("🚀 Divine Mirror AI - Simple Text Processor")
        print("=" * 50)
        print("Note: Using keyword-based search (no embeddings required)")
        
        # Find all text files
        text_files = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.txt'):
                    text_files.append(os.path.join(root, file))
        
        print(f"📚 Processing {len(text_files)} text files...")
        
        start_time = time.time()
        for filepath in text_files:
            self.process_file(filepath)
        
        elapsed = time.time() - start_time
        
        # Save index to file
        self.save_index()
        
        # Show statistics
        stats = self.index.get_statistics()
        print(f"\n📊 Processing Complete!")
        print(f"✅ Files processed: {self.processed_count}")
        print(f"📄 Total chunks: {self.chunk_count}")
        print(f"🔤 Unique words: {stats['total_words']}")
        print(f"⏱️ Time: {elapsed:.1f} seconds")
        
        print(f"\n🌍 Traditions processed:")
        for tradition, count in sorted(stats['traditions'].items()):
            print(f"   {tradition}: {count} chunks")
    
    def save_index(self, filename="divine_text_index.json"):
        """Save index to JSON file"""
        index_data = {
            'documents': self.index.documents,
            'metadata_index': self.index.metadata_index,
            'word_index': {word: list(doc_ids) for word, doc_ids in self.index.word_index.items()},
            'stats': self.index.get_statistics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Index saved to: {filename}")
    
    def test_search(self):
        """Test search functionality"""
        print(f"\n🔍 Testing Search Functionality")
        print("=" * 35)
        
        test_queries = [
            "Yeshua kingdom within heart",
            "Buddha suffering liberation enlightenment",
            "Tao nature harmony balance",
            "Hindu dharma consciousness divine",
            "love forgiveness compassion peace",
            "truth wisdom authentic teaching",
            "fear control manipulation institutional",
            "spirit soul divine inner light"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            results = self.index.search(query, max_results=3)
            
            if results:
                for i, result in enumerate(results, 1):
                    metadata = result['metadata']
                    tradition = metadata.get('tradition', 'Unknown')
                    title = metadata.get('title', 'Unknown')
                    score = result['score']
                    text = result['document'][:150] + "..."
                    
                    print(f"   {i}. [{tradition}] {title} (score: {score})")
                    print(f"      {text}")
            else:
                print("   No results found")

def main():
    """Main execution"""
    processor = DivineSimpleProcessor()
    processor.process_all_texts()
    processor.test_search()
    
    print(f"\n🎯 Divine Mirror AI simple search index ready!")
    print(f"Use divine_text_index.json for keyword-based search")

if __name__ == "__main__":
    main()