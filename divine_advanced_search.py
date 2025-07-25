#!/usr/bin/env python3
"""
Divine Mirror AI - Advanced Search Interface
Enhanced search with semantic tags and cross-tradition filtering
"""

import json
import re
from collections import defaultdict

class AdvancedSearchEngine:
    """Advanced search interface with semantic tagging support"""
    
    def __init__(self, enhanced_index_file="divine_enhanced_index.json"):
        self.load_enhanced_index(enhanced_index_file)
    
    def load_enhanced_index(self, filename):
        """Load the enhanced index with tags"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data['documents']
            self.metadata_index = data['metadata_index']
            self.word_index = {word: set(doc_ids) for word, doc_ids in data['word_index'].items()}
            self.stats = data['stats']
            self.tag_statistics = data.get('tag_statistics', {})
            
            print(f"✅ Loaded enhanced search: {len(self.documents)} tagged documents")
            
        except FileNotFoundError:
            print("❌ Enhanced index not found. Run divine_intelligent_tagger.py first.")
            self.documents = []
    
    def extract_words(self, text):
        """Extract search words from query"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {
            'the', 'and', 'but', 'for', 'are', 'with', 'his', 'they', 'this', 
            'have', 'from', 'one', 'had', 'were', 'been', 'their', 'said'
        }
        return [word for word in words if word not in stop_words]
    
    def search_by_tags(self, tag_filters, max_results=10):
        """Search documents by semantic tags"""
        results = []
        
        for doc in self.documents:
            tags = doc['metadata'].get('tags', [])
            
            # Check if document has all required tags
            if all(tag in tags for tag in tag_filters):
                results.append(doc)
        
        return results[:max_results]
    
    def advanced_search(self, query, filters=None, tag_filters=None, max_results=10):
        """Advanced search with multiple filter types"""
        if not self.documents:
            return []
        
        query_words = self.extract_words(query) if query else []
        doc_scores = defaultdict(int)
        
        # Score by text match if query provided
        if query_words:
            for word in query_words:
                if word in self.word_index:
                    for doc_id in self.word_index[word]:
                        doc_scores[doc_id] += 1
        else:
            # If no query, include all documents
            for doc in self.documents:
                doc_scores[doc['id']] = 1
        
        # Apply filters
        filtered_results = []
        for doc_id, score in doc_scores.items():
            doc = next((d for d in self.documents if d['id'] == doc_id), None)
            if not doc:
                continue
                
            metadata = doc['metadata']
            
            # Apply metadata filters
            if filters:
                matches_filter = True
                for key, value in filters.items():
                    if metadata.get(key, '').lower() != value.lower():
                        matches_filter = False
                        break
                if not matches_filter:
                    continue
            
            # Apply tag filters
            if tag_filters:
                doc_tags = metadata.get('tags', [])
                if not all(tag in doc_tags for tag in tag_filters):
                    continue
            
            filtered_results.append({
                'document': doc['text'],
                'metadata': metadata,
                'score': score
            })
        
        # Sort by relevance
        filtered_results.sort(key=lambda x: x['score'], reverse=True)
        return filtered_results[:max_results]
    
    def show_available_tags(self):
        """Show available semantic tags"""
        concept_tags = [tag for tag in self.tag_statistics.keys() 
                       if not tag.startswith(('tradition_', 'period_', 'type_'))]
        
        print("\n🏷️ Available Semantic Tags:")
        for i, tag in enumerate(sorted(concept_tags), 1):
            count = self.tag_statistics[tag]
            if i <= 30:  # Show top 30
                print(f"   {tag}: {count} documents")
    
    def show_traditions(self):
        """Show available traditions with counts"""
        tradition_tags = {tag: count for tag, count in self.tag_statistics.items() 
                         if tag.startswith('tradition_')}
        
        print("\n🌍 Available Traditions:")
        for tag, count in sorted(tradition_tags.items()):
            tradition = tag.replace('tradition_', '').title()
            print(f"   {tradition}: {count} documents")
    
    def interactive_search(self):
        """Interactive advanced search interface"""
        print("🔍 Divine Mirror AI - Advanced Search Engine")
        print("=" * 50)
        print("Enhanced search with semantic tags and cross-tradition analysis")
        print("Commands: 'search', 'tags', 'traditions', 'concept', 'help', 'quit'")
        
        while True:
            try:
                command = input("\n🔍 Enter command: ").strip().lower()
                
                if not command:
                    continue
                elif command in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'tags':
                    self.show_available_tags()
                elif command == 'traditions':
                    self.show_traditions()
                elif command == 'search':
                    self.handle_advanced_search()
                elif command == 'concept':
                    self.handle_concept_search()
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_advanced_search(self):
        """Handle advanced search with filters"""
        print("\n🔍 Advanced Search")
        query = input("Enter search query (optional): ").strip()
        
        print("\nOptional filters (press Enter to skip):")
        tradition = input("Tradition (e.g., Christianity, Buddhism): ").strip()
        period = input("Period (Ancient, Medieval, Modern): ").strip()
        
        print("\nSemantic tag filters (comma-separated, optional):")
        self.show_available_tags()
        tag_input = input("Enter tags: ").strip()
        
        # Build filters
        filters = {}
        if tradition:
            filters['tradition'] = tradition
        if period:
            filters['period'] = period
        
        tag_filters = []
        if tag_input:
            tag_filters = [tag.strip() for tag in tag_input.split(',')]
        
        # Perform search
        results = self.advanced_search(query, filters, tag_filters, max_results=10)
        
        print(f"\n🎯 Search Results ({len(results)} found):")
        
        if results:
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                tradition = metadata.get('tradition', 'Unknown')
                title = metadata.get('title', 'Unknown')
                period = metadata.get('period', 'Unknown')
                tags = metadata.get('tags', [])[:5]  # Show first 5 tags
                score = result['score']
                
                print(f"\n{i}. [{tradition}/{period}] {title} (relevance: {score})")
                print(f"   Tags: {', '.join(tags)}")
                
                # Show relevant excerpt
                text = result['document'][:300] + "..."
                print(f"   📖 {text}")
        else:
            print("   No results found. Try different search terms or filters.")
    
    def handle_concept_search(self):
        """Handle concept-based search"""
        print("\n📊 Concept Search")
        self.show_available_tags()
        
        concept = input("\nEnter concept tag: ").strip()
        
        if concept:
            results = self.search_by_tags([concept], max_results=10)
            
            print(f"\n🎯 Documents tagged with '{concept}' ({len(results)} found):")
            
            # Group by tradition
            tradition_groups = defaultdict(list)
            for doc in results:
                tradition = doc['metadata'].get('tradition', 'Unknown')
                tradition_groups[tradition].append(doc)
            
            for tradition, docs in tradition_groups.items():
                print(f"\n🔹 {tradition}: {len(docs)} documents")
                
                for doc in docs[:3]:  # Show first 3 per tradition
                    title = doc['metadata'].get('title', 'Unknown')
                    text = doc['text'][:200] + "..."
                    print(f"   📖 {title}: {text}")
    
    def show_help(self):
        """Show help information"""
        print("\n📖 Advanced Search Help:")
        print("   search      - Advanced search with filters")
        print("   concept     - Search by semantic concept")
        print("   tags        - Show available semantic tags")
        print("   traditions  - Show available traditions")
        print("   help        - Show this help")
        print("   quit        - Exit")
        print("\nExample searches:")
        print("   • Query: 'kingdom within' + Tradition: Christianity")
        print("   • Tags: divine_nature, love_compassion")
        print("   • Query: 'liberation' + Tags: salvation_liberation")

def main():
    """Main function"""
    engine = AdvancedSearchEngine()
    
    if engine.documents:
        engine.interactive_search()
    else:
        print("No enhanced index found. Please run divine_intelligent_tagger.py first.")

if __name__ == "__main__":
    main()