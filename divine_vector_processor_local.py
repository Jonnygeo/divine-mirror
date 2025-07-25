#!/usr/bin/env python3
"""
Divine Mirror AI - Local Vector Database Processor
Processes all sacred texts into ChromaDB using local embeddings (no API quota needed)
"""

import os
import json
import chromadb
from chromadb.config import Settings
import tiktoken
from pathlib import Path
import time
import numpy as np
from sentence_transformers import SentenceTransformer

# Configuration
CHUNK_SIZE = 512  # tokens per chunk
DB_DIR = "chromadb_storage"
MODEL_NAME = "all-MiniLM-L6-v2"  # Small, fast local embedding model

class LocalEmbeddingFunction:
    """Local embedding function using sentence-transformers"""
    
    def __init__(self, model_name=MODEL_NAME):
        print(f"🔄 Loading local embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("✅ Local embedding model loaded successfully")
    
    def __call__(self, texts):
        """Generate embeddings for given texts"""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

class DivineVectorProcessor:
    def __init__(self):
        """Initialize the vector processor with local embeddings"""
        self.setup_chromadb()
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.processed_count = 0
        self.error_count = 0
        self.chunk_count = 0
        
    def setup_chromadb(self):
        """Initialize ChromaDB client and collection with local embeddings"""
        try:
            # Create persistent ChromaDB client
            self.client = chromadb.PersistentClient(path=DB_DIR)
            
            # Setup local embedding function
            self.embedding_function = LocalEmbeddingFunction()
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection("sacred_texts_local")
                print(f"📚 Found existing local collection with {self.collection.count()} documents")
            except:
                self.collection = self.client.create_collection(
                    name="sacred_texts_local",
                    embedding_function=self.embedding_function
                )
                print("📚 Created new sacred_texts_local collection with local embeddings")
                
        except Exception as e:
            print(f"❌ Error setting up ChromaDB: {e}")
            raise
    
    def tokenize_text(self, text):
        """Tokenize text using tiktoken"""
        try:
            return self.tokenizer.encode(text)
        except Exception as e:
            return text.split()  # Fallback to word splitting
    
    def chunk_text(self, text, size=CHUNK_SIZE):
        """Split text into chunks of specified token size"""
        tokens = self.tokenize_text(text)
        chunks = []
        
        for i in range(0, len(tokens), size):
            chunk_tokens = tokens[i:i+size]
            try:
                chunk_text = self.tokenizer.decode(chunk_tokens)
            except:
                # Fallback: join tokens as strings
                chunk_text = " ".join([str(t) for t in chunk_tokens])
            chunks.append(chunk_text)
        
        return chunks
    
    def extract_metadata(self, filepath):
        """Extract metadata from file path and content"""
        path_parts = Path(filepath).parts
        
        # Parse path structure: data/texts/Tradition/Period/Type/filename.txt
        if len(path_parts) >= 5:
            tradition = path_parts[2]
            period = path_parts[3]
            text_type = path_parts[4]
        else:
            tradition = "Unknown"
            period = "Unknown"
            text_type = "Unknown"
        
        filename = Path(filepath).stem
        
        # Enhanced metadata
        metadata = {
            "tradition": tradition,
            "period": period,
            "type": text_type,
            "title": filename,
            "source_path": str(filepath),
            "filename": Path(filepath).name
        }
        
        # Add tradition-specific metadata
        if tradition == "Christianity":
            metadata["tradition_family"] = "Abrahamic"
        elif tradition in ["Judaism", "Islam"]:
            metadata["tradition_family"] = "Abrahamic"
        elif tradition in ["Hinduism", "Buddhism", "Jainism", "Sikhism"]:
            metadata["tradition_family"] = "Dharmic"
        elif tradition in ["Taoism", "Confucianism", "Shinto"]:
            metadata["tradition_family"] = "East_Asian"
        else:
            metadata["tradition_family"] = "Other"
        
        return metadata
    
    def process_file(self, filepath):
        """Process a single file into vector chunks"""
        try:
            print(f"📄 Processing: {Path(filepath).name}")
            
            # Read file content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
            
            if not content or len(content) < 50:
                print(f"⏭️ Skipping empty/small file: {filepath}")
                return 0
            
            # Extract metadata
            base_metadata = self.extract_metadata(filepath)
            
            # Create text chunks
            chunks = self.chunk_text(content)
            chunks_added = 0
            
            # Process chunks in batches for efficiency
            batch_size = 10
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i+batch_size]
                batch_docs = []
                batch_metadatas = []
                batch_ids = []
                
                for j, chunk in enumerate(batch_chunks):
                    if len(chunk.strip()) < 10:  # Skip tiny chunks
                        continue
                    
                    # Create unique document ID
                    chunk_idx = i + j
                    doc_id = f"{base_metadata['tradition']}_{base_metadata['title']}_{chunk_idx}"
                    
                    # Add chunk-specific metadata
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata.update({
                        "chunk_id": chunk_idx,
                        "total_chunks": len(chunks),
                        "chunk_length": len(chunk)
                    })
                    
                    batch_docs.append(chunk)
                    batch_metadatas.append(chunk_metadata)
                    batch_ids.append(doc_id)
                
                # Add batch to ChromaDB
                if batch_docs:
                    try:
                        self.collection.add(
                            documents=batch_docs,
                            metadatas=batch_metadatas,
                            ids=batch_ids
                        )
                        chunks_added += len(batch_docs)
                        self.chunk_count += len(batch_docs)
                    except Exception as e:
                        print(f"❌ Error adding batch: {e}")
                        self.error_count += len(batch_docs)
            
            self.processed_count += 1
            print(f"✅ Added {chunks_added} chunks from {Path(filepath).name}")
            return chunks_added
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            self.error_count += 1
            return 0
    
    def process_all_texts(self, base_dir="data/texts"):
        """Process all text files in the sacred texts directory"""
        print("🚀 Divine Mirror AI - Local Vector Database Processing")
        print("=" * 60)
        
        # Find all text files
        text_files = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.txt') and file != 'README.md':
                    text_files.append(os.path.join(root, file))
        
        print(f"📚 Found {len(text_files)} text files to process")
        
        # Process each file
        total_chunks = 0
        start_time = time.time()
        
        for i, filepath in enumerate(text_files, 1):
            print(f"\n[{i}/{len(text_files)}] Processing file...")
            chunks_added = self.process_file(filepath)
            total_chunks += chunks_added
            
            # Progress update every 20 files
            if i % 20 == 0 or i == len(text_files):
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                print(f"⏱️ Progress: {i}/{len(text_files)} files ({elapsed:.1f}s, {rate:.1f} files/sec)")
        
        # Final summary
        elapsed = time.time() - start_time
        print(f"\n📊 Processing Complete!")
        print(f"=" * 35)
        print(f"✅ Files processed: {self.processed_count}")
        print(f"❌ Errors: {self.error_count}")
        print(f"📄 Total chunks: {self.chunk_count}")
        print(f"⏱️ Time elapsed: {elapsed:.1f} seconds")
        print(f"💾 Database location: {DB_DIR}")
        
        # Verify final collection size
        try:
            final_count = self.collection.count()
            print(f"🔍 ChromaDB verification: {final_count} documents stored")
        except Exception as e:
            print(f"⚠️ Could not verify collection size: {e}")
    
    def test_search(self):
        """Test the search functionality"""
        print("\n🔍 Testing semantic search with local embeddings...")
        
        test_queries = [
            "What did Yeshua say about the kingdom within?",
            "Buddhist teachings on suffering and liberation",
            "Taoist concept of wu wei and natural action",
            "Hindu concept of dharma and righteous duty",
            "Islamic teachings on divine compassion"
        ]
        
        for query in test_queries:
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=3
                )
                
                print(f"\n🔍 Query: '{query}'")
                if results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        tradition = metadata.get('tradition', 'Unknown')
                        title = metadata.get('title', 'Unknown')
                        print(f"  {i+1}. [{tradition}] {title}: {doc[:100]}...")
                else:
                    print("  No results found")
                    
            except Exception as e:
                print(f"❌ Search error for '{query}': {e}")

def main():
    """Main execution function"""
    print("🌟 Divine Mirror AI - Local Vector Processing (No API Quota Required)")
    print("Using local sentence-transformers for embeddings")
    print("")
    
    processor = DivineVectorProcessor()
    
    # Process all texts
    processor.process_all_texts()
    
    # Test search functionality
    processor.test_search()
    
    print(f"\n🎯 Divine Mirror AI local vector database ready!")
    print(f"Collection: sacred_texts_local")
    print(f"Use this collection for offline semantic search across all sacred texts.")

if __name__ == "__main__":
    main()