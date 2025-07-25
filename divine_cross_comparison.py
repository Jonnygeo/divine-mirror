#!/usr/bin/env python3
"""
Divine Mirror AI - Cross-Text Comparison Engine
Advanced comparison system for analyzing teachings across religious traditions
"""

import json
import re
from collections import defaultdict, Counter

class CrossTextComparator:
    """Advanced comparison engine for sacred texts"""
    
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
            
            print(f"✅ Loaded enhanced index with {len(self.documents)} tagged documents")
            
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
    
    def search_by_concept(self, concept_tag, max_results=10):
        """Search for documents containing a specific concept tag"""
        results = []
        
        for doc in self.documents:
            tags = doc['metadata'].get('tags', [])
            if concept_tag in tags:
                results.append(doc)
        
        return results[:max_results]
    
    def compare_traditions(self, query, tradition_a, tradition_b, max_results_each=5):
        """Compare how two traditions handle a specific query"""
        
        # Search in tradition A
        results_a = self.search_with_filter(query, {"tradition": tradition_a}, max_results_each)
        
        # Search in tradition B  
        results_b = self.search_with_filter(query, {"tradition": tradition_b}, max_results_each)
        
        return {
            'query': query,
            'tradition_a': tradition_a,
            'tradition_b': tradition_b,
            'results_a': results_a,
            'results_b': results_b
        }
    
    def search_with_filter(self, query, filters, max_results=5):
        """Search with metadata filters"""
        query_words = self.extract_words(query)
        if not query_words:
            return []
        
        doc_scores = defaultdict(int)
        
        # Score documents by word matches
        for word in query_words:
            if word in self.word_index:
                for doc_id in self.word_index[word]:
                    doc_scores[doc_id] += 1
        
        # Apply filters
        filtered_results = []
        for doc_id, score in doc_scores.items():
            doc = next((d for d in self.documents if d['id'] == doc_id), None)
            if doc:
                metadata = doc['metadata']
                
                # Check if document matches all filters
                matches_filter = True
                for key, value in filters.items():
                    if metadata.get(key, '').lower() != value.lower():
                        matches_filter = False
                        break
                
                if matches_filter:
                    filtered_results.append({
                        'document': doc['text'],
                        'metadata': metadata,
                        'score': score
                    })
        
        # Sort by relevance and return top results
        filtered_results.sort(key=lambda x: x['score'], reverse=True)
        return filtered_results[:max_results]
    
    def analyze_concept_across_traditions(self, concept_tag):
        """Analyze how a concept appears across different traditions"""
        
        concept_docs = self.search_by_concept(concept_tag)
        
        if not concept_docs:
            return None
        
        # Group by tradition
        tradition_analysis = defaultdict(list)
        
        for doc in concept_docs:
            tradition = doc['metadata'].get('tradition', 'Unknown')
            tradition_analysis[tradition].append({
                'text': doc['text'][:300] + "...",
                'title': doc['metadata'].get('title', 'Unknown'),
                'period': doc['metadata'].get('period', 'Unknown'),
                'tags': doc['metadata'].get('tags', [])
            })
        
        return {
            'concept': concept_tag,
            'total_documents': len(concept_docs),
            'traditions_found': len(tradition_analysis),
            'tradition_breakdown': dict(tradition_analysis)
        }
    
    def find_manipulation_patterns(self):
        """Identify manipulation patterns across traditions"""
        
        manipulation_tags = [
            'fear_based', 'authority_control', 'material_focus',
            'guilt_shame', 'obedience_submission'
        ]
        
        manipulation_analysis = {}
        
        for tag in manipulation_tags:
            tag_docs = self.search_by_concept(tag)
            
            if tag_docs:
                tradition_breakdown = defaultdict(int)
                for doc in tag_docs:
                    tradition = doc['metadata'].get('tradition', 'Unknown')
                    tradition_breakdown[tradition] += 1
                
                manipulation_analysis[tag] = {
                    'total_documents': len(tag_docs),
                    'tradition_breakdown': dict(tradition_breakdown),
                    'examples': [
                        {
                            'tradition': doc['metadata'].get('tradition', 'Unknown'),
                            'title': doc['metadata'].get('title', 'Unknown'),
                            'excerpt': doc['text'][:200] + "..."
                        }
                        for doc in tag_docs[:3]  # Show top 3 examples
                    ]
                }
        
        return manipulation_analysis
    
    def compare_original_vs_institutional(self, concept):
        """Compare original teachings vs institutional interpretations"""
        
        # Search for original period texts
        original_results = self.search_with_filter(concept, {"period": "Ancient"}, max_results=5)
        
        # Search for later institutional texts
        institutional_results = self.search_with_filter(concept, {"period": "Medieval"}, max_results=5)
        
        if not institutional_results:
            # Try "Modern" period if Medieval not found
            institutional_results = self.search_with_filter(concept, {"period": "Modern"}, max_results=5)
        
        return {
            'concept': concept,
            'original_teachings': original_results,
            'institutional_interpretations': institutional_results,
            'comparison_available': len(original_results) > 0 and len(institutional_results) > 0
        }
    
    def interactive_comparison(self):
        """Interactive comparison interface"""
        print("🔄 Divine Mirror AI - Cross-Text Comparison Engine")
        print("=" * 55)
        print("Advanced comparison system for analyzing teachings across traditions")
        print("Commands: 'concept', 'compare', 'manipulation', 'original', 'help', 'quit'")
        
        while True:
            try:
                command = input("\n🔄 Enter command: ").strip().lower()
                
                if not command:
                    continue
                elif command in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'concept':
                    self.handle_concept_analysis()
                elif command == 'compare':
                    self.handle_tradition_comparison()
                elif command == 'manipulation':
                    self.handle_manipulation_analysis()
                elif command == 'original':
                    self.handle_original_vs_institutional()
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_concept_analysis(self):
        """Handle concept analysis command"""
        print("\n📊 Available concepts:")
        concepts = [tag for tag in self.tag_statistics.keys() 
                   if not tag.startswith(('tradition_', 'period_', 'type_'))][:20]
        
        for i, concept in enumerate(concepts, 1):
            count = self.tag_statistics[concept]
            print(f"   {i}. {concept} ({count} docs)")
        
        concept = input("\nEnter concept name: ").strip()
        
        if concept:
            analysis = self.analyze_concept_across_traditions(concept)
            
            if analysis:
                print(f"\n📋 Analysis of '{concept}':")
                print(f"   Total documents: {analysis['total_documents']}")
                print(f"   Traditions found: {analysis['traditions_found']}")
                
                for tradition, docs in analysis['tradition_breakdown'].items():
                    print(f"\n   🔹 {tradition}: {len(docs)} documents")
                    for doc in docs[:2]:  # Show first 2 examples
                        print(f"      📖 {doc['title']}: {doc['text']}")
            else:
                print(f"No documents found for concept '{concept}'")
    
    def handle_tradition_comparison(self):
        """Handle tradition comparison command"""
        traditions = list(set(doc['metadata'].get('tradition', 'Unknown') 
                            for doc in self.documents))
        
        print(f"\n🌍 Available traditions: {', '.join(sorted(traditions))}")
        
        tradition_a = input("Enter first tradition: ").strip()
        tradition_b = input("Enter second tradition: ").strip()
        query = input("Enter concept to compare: ").strip()
        
        if tradition_a and tradition_b and query:
            comparison = self.compare_traditions(query, tradition_a, tradition_b)
            
            print(f"\n⚖️ Comparing '{query}' between {tradition_a} and {tradition_b}:")
            
            print(f"\n🔵 {tradition_a} Perspective:")
            for i, result in enumerate(comparison['results_a'], 1):
                metadata = result['metadata']
                print(f"   {i}. {metadata['title']}: {result['document'][:150]}...")
            
            print(f"\n🔴 {tradition_b} Perspective:")
            for i, result in enumerate(comparison['results_b'], 1):
                metadata = result['metadata']
                print(f"   {i}. {metadata['title']}: {result['document'][:150]}...")
    
    def handle_manipulation_analysis(self):
        """Handle manipulation pattern analysis"""
        print("\n🕵️ Analyzing manipulation patterns across traditions...")
        
        patterns = self.find_manipulation_patterns()
        
        for pattern, data in patterns.items():
            print(f"\n🚨 {pattern.replace('_', ' ').title()}:")
            print(f"   Total documents: {data['total_documents']}")
            print(f"   Tradition breakdown:")
            
            for tradition, count in data['tradition_breakdown'].items():
                print(f"      {tradition}: {count} documents")
            
            if data['examples']:
                print("   Examples:")
                for example in data['examples']:
                    print(f"      📖 [{example['tradition']}] {example['title']}")
                    print(f"         {example['excerpt']}")
    
    def handle_original_vs_institutional(self):
        """Handle original vs institutional comparison"""
        concept = input("Enter concept to analyze (e.g., 'salvation', 'hell', 'love'): ").strip()
        
        if concept:
            comparison = self.compare_original_vs_institutional(concept)
            
            print(f"\n📚 Original vs Institutional: '{concept}'")
            
            if comparison['comparison_available']:
                print(f"\n🏛️ Original/Ancient Teachings:")
                for i, result in enumerate(comparison['original_teachings'], 1):
                    metadata = result['metadata']
                    tradition = metadata.get('tradition', 'Unknown')
                    title = metadata.get('title', 'Unknown')
                    print(f"   {i}. [{tradition}] {title}: {result['document'][:150]}...")
                
                print(f"\n🏛️ Institutional Interpretations:")
                for i, result in enumerate(comparison['institutional_interpretations'], 1):
                    metadata = result['metadata']
                    tradition = metadata.get('tradition', 'Unknown')
                    title = metadata.get('title', 'Unknown')
                    print(f"   {i}. [{tradition}] {title}: {result['document'][:150]}...")
            else:
                print("Insufficient data for comparison. Try a different concept.")
    
    def show_help(self):
        """Show help information"""
        print("\n📖 Comparison Engine Help:")
        print("   concept  - Analyze how a concept appears across traditions")
        print("   compare  - Compare two traditions' approach to a topic")
        print("   manipulation - Identify manipulation patterns")
        print("   original - Compare original vs institutional teachings")
        print("   help     - Show this help")
        print("   quit     - Exit")

def main():
    """Main function"""
    comparator = CrossTextComparator()
    
    if comparator.documents:
        comparator.interactive_comparison()
    else:
        print("No enhanced index found. Please run divine_intelligent_tagger.py first.")

if __name__ == "__main__":
    main()