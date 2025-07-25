#!/usr/bin/env python3
"""
Divine Mirror AI - Phase 4: Vector Database Processor
Processes all sacred texts into ChromaDB for semantic search
"""

import os
import json
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import tiktoken
from pathlib import Path
import time

# Configuration
CHUNK_SIZE = 512  # tokens per chunk
DB_DIR = "chromadb_storage"
MAX_RETRIES = 3
RETRY_DELAY = 2

class DivineVectorProcessor:
    def __init__(self):
        """Initialize the vector processor"""
        self.setup_chromadb()
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.processed_count = 0
        self.error_count = 0
        self.chunk_count = 0
        
    def setup_chromadb(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create persistent ChromaDB client
            self.client = chromadb.PersistentClient(path=DB_DIR)
            
            # Setup OpenAI embedding function
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                print("⚠️ No OpenAI API key found. Using default embeddings.")
                self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
            else:
                self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=openai_api_key,
                    model_name="text-embedding-3-small"  # More cost-effective
                )
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection("sacred_texts")
                print(f"📚 Found existing collection with {self.collection.count()} documents")
            except:
                self.collection = self.client.create_collection(
                    name="sacred_texts",
                    embedding_function=self.embedding_function
                )
                print("📚 Created new sacred_texts collection")
                
        except Exception as e:
            print(f"❌ Error setting up ChromaDB: {e}")
            raise
    
    def tokenize_text(self, text):
        """Tokenize text using tiktoken"""
        try:
            return self.tokenizer.encode(text)
        except Exception as e:
            print(f"⚠️ Tokenization error: {e}")
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
            
            # Add each chunk to ChromaDB
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) < 10:  # Skip tiny chunks
                    continue
                
                # Create unique document ID
                doc_id = f"{base_metadata['tradition']}_{base_metadata['title']}_{i}"
                
                # Add chunk-specific metadata
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "chunk_length": len(chunk)
                })
                
                # Retry logic for API failures
                for attempt in range(MAX_RETRIES):
                    try:
                        self.collection.add(
                            documents=[chunk],
                            metadatas=[chunk_metadata],
                            ids=[doc_id]
                        )
                        chunks_added += 1
                        self.chunk_count += 1
                        break
                    except Exception as e:
                        if attempt < MAX_RETRIES - 1:
                            print(f"⚠️ Retry {attempt + 1} for chunk {i}: {e}")
                            time.sleep(RETRY_DELAY)
                        else:
                            print(f"❌ Failed to add chunk {i}: {e}")
                            self.error_count += 1
            
            self.processed_count += 1
            print(f"✅ Added {chunks_added} chunks from {Path(filepath).name}")
            return chunks_added
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            self.error_count += 1
            return 0
    
    def process_all_texts(self, base_dir="data/texts"):
        """Process all text files in the sacred texts directory"""
        print("🚀 Divine Mirror AI - Vector Database Processing")
        print("=" * 55)
        
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
            
            # Progress update every 10 files
            if i % 10 == 0:
                elapsed = time.time() - start_time
                print(f"⏱️ Progress: {i}/{len(text_files)} files ({elapsed:.1f}s)")
        
        # Final summary
        elapsed = time.time() - start_time
        print(f"\n📊 Processing Complete!")
        print(f"=" * 30)
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
        print("\n🔍 Testing semantic search...")
        
        test_queries = [
            "What did Yeshua say about the kingdom within?",
            "Buddhist teachings on suffering",
            "Taoist concept of wu wei",
            "Hindu concept of dharma"
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
    processor = DivineVectorProcessor()
    
    # Process all texts
    processor.process_all_texts()
    
    # Test search functionality
    processor.test_search()
    
    print(f"\n🎯 Divine Mirror AI vector database ready!")
    print(f"Use the ChromaDB collection for semantic search across all sacred texts.")

if __name__ == "__main__":
    main()