#!/usr/bin/env python3
"""
Divine Mirror AI - Sacred Text Search Interface
Interactive search tool for the processed sacred texts
"""

import json
import re
from collections import defaultdict

class SacredTextSearcher:
    """Interactive search interface for sacred texts"""
    
    def __init__(self, index_file="divine_text_index.json"):
        self.load_index(index_file)
    
    def load_index(self, filename):
        """Load the text index from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data['documents']
            self.metadata_index = data['metadata_index']
            self.word_index = {word: set(doc_ids) for word, doc_ids in data['word_index'].items()}
            self.stats = data['stats']
            
            print(f"✅ Loaded index: {self.stats['total_documents']} documents")
            
        except FileNotFoundError:
            print("❌ Index file not found. Run divine_simple_processor.py first.")
            self.documents = []
            self.metadata_index = {}
            self.word_index = {}
            self.stats = {}
    
    def extract_words(self, text):
        """Extract search words from query"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {
            'the', 'and', 'but', 'for', 'are', 'with', 'his', 'they', 'this', 
            'have', 'from', 'one', 'had', 'were', 'been', 'their', 'said'
        }
        return [word for word in words if word not in stop_words]
    
    def search(self, query, max_results=5, tradition_filter=None):
        """Search for documents matching query"""
        if not self.documents:
            return []
        
        query_words = self.extract_words(query)
        if not query_words:
            return []
        
        doc_scores = defaultdict(int)
        
        # Score documents by word matches
        for word in query_words:
            if word in self.word_index:
                for doc_id in self.word_index[word]:
                    doc_scores[doc_id] += 1
        
        # Apply tradition filter if specified
        if tradition_filter:
            filtered_scores = {}
            for doc_id, score in doc_scores.items():
                if doc_id in self.metadata_index:
                    tradition = self.metadata_index[doc_id].get('tradition', '')
                    if tradition.lower() == tradition_filter.lower():
                        filtered_scores[doc_id] = score
            doc_scores = filtered_scores
        
        # Sort by relevance
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return results
        results = []
        for doc_id, score in sorted_docs[:max_results]:
            doc = next((d for d in self.documents if d['id'] == doc_id), None)
            if doc:
                results.append({
                    'document': doc['text'],
                    'metadata': doc['metadata'],
                    'score': score
                })
        
        return results
    
    def show_traditions(self):
        """Show available traditions"""
        if 'traditions' in self.stats:
            print("\n🌍 Available Traditions:")
            for tradition, count in sorted(self.stats['traditions'].items()):
                print(f"   {tradition}: {count} chunks")
    
    def interactive_search(self):
        """Interactive search interface"""
        print("🔍 Divine Mirror AI - Sacred Text Search")
        print("=" * 45)
        print("Search across 164 sacred texts from 17 religious traditions")
        print("Commands: 'help', 'traditions', 'quit'")
        
        while True:
            try:
                query = input("\n🔍 Enter search query: ").strip()
                
                if not query:
                    continue
                elif query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif query.lower() == 'help':
                    self.show_help()
                elif query.lower() == 'traditions':
                    self.show_traditions()
                elif query.startswith('filter:'):
                    # Format: filter:Christianity search terms here
                    parts = query.split(':', 1)[1].split(' ', 1)
                    if len(parts) == 2:
                        tradition, search_query = parts
                        self.perform_search(search_query.strip(), tradition.strip())
                    else:
                        print("Format: filter:TraditionName search terms")
                else:
                    self.perform_search(query)
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def perform_search(self, query, tradition_filter=None):
        """Perform and display search results"""
        results = self.search(query, max_results=5, tradition_filter=tradition_filter)
        
        if tradition_filter:
            print(f"\n🎯 Results for '{query}' in {tradition_filter}:")
        else:
            print(f"\n🎯 Results for '{query}':")
        
        if results:
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                tradition = metadata.get('tradition', 'Unknown')
                title = metadata.get('title', 'Unknown')
                period = metadata.get('period', 'Unknown')
                score = result['score']
                
                print(f"\n{i}. [{tradition}/{period}] {title} (relevance: {score})")
                
                # Show relevant excerpt
                text = result['document']
                query_words = self.extract_words(query)
                
                # Find best excerpt containing query words
                sentences = text.split('. ')
                best_sentence = ""
                max_word_count = 0
                
                for sentence in sentences:
                    word_count = sum(1 for word in query_words if word in sentence.lower())
                    if word_count > max_word_count:
                        max_word_count = word_count
                        best_sentence = sentence
                
                if best_sentence:
                    excerpt = best_sentence[:300] + "..."
                else:
                    excerpt = text[:300] + "..."
                
                print(f"   📖 {excerpt}")
        else:
            print("   No results found.")
            print("   Try different keywords or check available traditions.")
    
    def show_help(self):
        """Show help information"""
        print("\n📖 Search Help:")
        print("   • Enter keywords to search across all texts")
        print("   • Use 'filter:TraditionName search terms' for tradition-specific search")
        print("   • Example: 'filter:Christianity kingdom within'")
        print("   • Type 'traditions' to see available traditions")
        print("   • Type 'quit' to exit")

def main():
    """Main function"""
    searcher = SacredTextSearcher()
    
    if searcher.documents:
        searcher.interactive_search()
    else:
        print("No search index found. Please run divine_simple_processor.py first.")

if __name__ == "__main__":
    main()