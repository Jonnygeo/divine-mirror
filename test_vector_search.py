#!/usr/bin/env python3
"""
Divine Mirror AI - Vector Search Test
Tests the local vector database search capabilities
"""

import chromadb
from pathlib import Path

def test_vector_database():
    """Test the local vector database functionality"""
    
    print("🔍 Divine Mirror AI - Vector Search Test")
    print("=" * 45)
    
    try:
        # Connect to ChromaDB
        client = chromadb.PersistentClient(path="chromadb_storage")
        collection = client.get_collection("sacred_texts_local")
        
        # Get collection stats
        count = collection.count()
        print(f"📚 Database contains {count} text chunks")
        
        if count == 0:
            print("⚠️ No documents found. Run divine_vector_processor_local.py first.")
            return
        
        # Test queries for cross-religious truth analysis
        test_queries = [
            "Yeshua teachings about love and forgiveness",
            "Buddha's teachings on suffering and enlightenment", 
            "Taoist philosophy of natural harmony",
            "Hindu concept of divine consciousness",
            "Original Christianity versus institutional corruption",
            "Kingdom of heaven within versus external authority",
            "Universal spiritual truths across traditions",
            "Religious manipulation and fear-based control",
            "Direct spiritual experience versus mediated religion",
            "Sacred feminine divine wisdom"
        ]
        
        print("\n🎯 Cross-Religious Truth Analysis Tests:")
        print("=" * 45)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            
            try:
                results = collection.query(
                    query_texts=[query],
                    n_results=5
                )
                
                if results['documents'][0]:
                    traditions_found = set()
                    
                    for j, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][j]
                        tradition = metadata.get('tradition', 'Unknown')
                        title = metadata.get('title', 'Unknown')
                        traditions_found.add(tradition)
                        
                        # Show first result in detail, others abbreviated
                        if j == 0:
                            print(f"   🎯 [{tradition}] {title}")
                            print(f"      {doc[:200]}...")
                        else:
                            print(f"   📖 [{tradition}] {title}: {doc[:80]}...")
                    
                    print(f"   🌍 Traditions found: {', '.join(sorted(traditions_found))}")
                else:
                    print("   ❌ No results found")
                    
            except Exception as e:
                print(f"   ❌ Search error: {e}")
        
        # Test tradition-specific filtering
        print(f"\n🏛️ Tradition-Specific Analysis:")
        print("=" * 35)
        
        # Get available traditions
        all_results = collection.get()
        traditions = set()
        if all_results['metadatas']:
            for metadata in all_results['metadatas'][:100]:  # Sample first 100
                tradition = metadata.get('tradition')
                if tradition:
                    traditions.add(tradition)
        
        print(f"Available traditions: {', '.join(sorted(traditions))}")
        
        # Test filtering by tradition
        if 'Christianity' in traditions:
            print(f"\n📜 Christianity-specific search: 'Kingdom within'")
            results = collection.query(
                query_texts=["kingdom within"],
                n_results=3,
                where={"tradition": "Christianity"}
            )
            
            if results['documents'][0]:
                for doc in results['documents'][0]:
                    print(f"   📖 {doc[:100]}...")
        
        print(f"\n✅ Vector database test completed successfully!")
        print(f"🎯 Your Divine Mirror AI is ready for truth analysis!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print("Make sure to run divine_vector_processor_local.py first")

if __name__ == "__main__":
    test_vector_database()