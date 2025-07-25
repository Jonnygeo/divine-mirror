#!/usr/bin/env python3
"""
Divine Mirror AI - Phase 7: Spiritual Forensics Search Engine
Advanced search by symbol, spiritual law, theme, and verse reference
"""

import json
import re
from collections import defaultdict, Counter

class SpiritualForensicsEngine:
    """Advanced forensics search engine for spiritual analysis"""
    
    def __init__(self, forensic_index_file="divine_forensic_index.json"):
        self.load_forensic_index(forensic_index_file)
        
    def load_forensic_index(self, filename):
        """Load the forensic index with enhanced metadata"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data['documents']
            self.metadata_index = data['metadata_index']
            self.forensic_stats = data.get('forensic_statistics', {})
            self.symbol_dictionary = data.get('symbol_dictionary', {})
            self.spiritual_laws = data.get('spiritual_laws_reference', {})
            
            print(f"🔬 Loaded forensic database: {len(self.documents)} spiritually analyzed documents")
            
        except FileNotFoundError:
            print("❌ Forensic index not found. Run divine_metadata_generator.py first.")
            self.documents = []
    
    def search_by_symbol(self, symbol, max_results=10):
        """Search for documents containing specific symbols"""
        results = []
        
        for doc in self.documents:
            symbols = doc['metadata'].get('symbols', [])
            if symbol in symbols:
                result = {
                    'document': doc['text'][:300] + "...",
                    'metadata': doc['metadata'],
                    'symbol_context': self.get_symbol_context(doc['text'], symbol),
                    'cross_traditions': doc['metadata'].get('cross_tradition_links', {}),
                    'related_symbols': [s for s in symbols if s != symbol][:3]
                }
                results.append(result)
        
        return results[:max_results]
    
    def search_by_spiritual_law(self, law, max_results=10):
        """Search for documents containing specific spiritual laws"""
        results = []
        
        for doc in self.documents:
            laws = doc['metadata'].get('spiritual_laws', [])
            if law in laws:
                result = {
                    'document': doc['text'][:300] + "...",
                    'metadata': doc['metadata'],
                    'law_context': self.get_law_context(doc['text'], law),
                    'tradition': doc['metadata'].get('tradition', 'Unknown'),
                    'related_laws': [l for l in laws if l != law][:2]
                }
                results.append(result)
        
        return results[:max_results]
    
    def search_by_verse_reference(self, verse_ref):
        """Search for specific verse references"""
        results = []
        
        # Normalize verse reference
        verse_ref_clean = verse_ref.strip().lower()
        
        for doc in self.documents:
            key_verses = doc['metadata'].get('key_verses', {})
            
            for verse_key, verse_text in key_verses.items():
                if verse_ref_clean in verse_key.lower() or verse_key.lower() in verse_ref_clean:
                    result = {
                        'verse_reference': verse_key,
                        'verse_text': verse_text,
                        'source': doc['metadata'].get('title', 'Unknown'),
                        'tradition': doc['metadata'].get('tradition', 'Unknown'),
                        'period': doc['metadata'].get('period', 'Unknown'),
                        'document_context': doc['text'][:200] + "..."
                    }
                    results.append(result)
        
        return results
    
    def search_by_theme(self, theme, max_results=10):
        """Search for documents by spiritual theme"""
        results = []
        
        for doc in self.documents:
            themes = doc['metadata'].get('themes', [])
            if theme in themes:
                result = {
                    'document': doc['text'][:300] + "...",
                    'metadata': doc['metadata'],
                    'primary_themes': themes[:5],
                    'symbols_present': doc['metadata'].get('symbols', [])[:3],
                    'laws_present': doc['metadata'].get('spiritual_laws', [])[:2]
                }
                results.append(result)
        
        return results[:max_results]
    
    def forensic_comparison(self, element_type, element_name):
        """Compare how an element appears across traditions"""
        
        tradition_analysis = defaultdict(list)
        
        for doc in self.documents:
            tradition = doc['metadata'].get('tradition', 'Unknown')
            
            if element_type == 'symbol':
                elements = doc['metadata'].get('symbols', [])
            elif element_type == 'law':
                elements = doc['metadata'].get('spiritual_laws', [])
            elif element_type == 'theme':
                elements = doc['metadata'].get('themes', [])
            else:
                continue
            
            if element_name in elements:
                analysis_item = {
                    'source': doc['metadata'].get('title', 'Unknown'),
                    'period': doc['metadata'].get('period', 'Unknown'),
                    'excerpt': doc['text'][:200] + "...",
                    'context': self.get_element_context(doc['text'], element_name)
                }
                tradition_analysis[tradition].append(analysis_item)
        
        return {
            'element_type': element_type,
            'element_name': element_name,
            'traditions_found': len(tradition_analysis),
            'tradition_breakdown': dict(tradition_analysis)
        }
    
    def universal_archetype_analysis(self):
        """Analyze universal archetypes across all traditions"""
        
        symbol_analysis = {}
        
        for symbol, data in self.symbol_dictionary.items():
            if len(data['traditions']) >= 3:  # Universal if in 3+ traditions
                
                # Find documents containing this symbol
                symbol_docs = self.search_by_symbol(symbol, max_results=20)
                
                if symbol_docs:
                    tradition_contexts = defaultdict(list)
                    
                    for doc in symbol_docs:
                        tradition = doc['metadata']['tradition']
                        tradition_contexts[tradition].append({
                            'source': doc['metadata']['title'],
                            'context': doc['symbol_context']
                        })
                    
                    symbol_analysis[symbol] = {
                        'universal_meanings': data['meanings'],
                        'traditions_with_symbol': list(tradition_contexts.keys()),
                        'total_occurrences': len(symbol_docs),
                        'tradition_contexts': dict(tradition_contexts)
                    }
        
        return symbol_analysis
    
    def spiritual_law_comparison(self):
        """Compare spiritual laws across traditions"""
        
        law_comparison = {}
        
        for law, data in self.spiritual_laws.items():
            if len(data['traditions']) >= 3:  # Universal if in 3+ traditions
                
                law_docs = self.search_by_spiritual_law(law, max_results=15)
                
                if law_docs:
                    tradition_applications = defaultdict(list)
                    
                    for doc in law_docs:
                        tradition = doc['tradition']
                        tradition_applications[tradition].append({
                            'source': doc['metadata']['title'],
                            'application': doc['law_context']
                        })
                    
                    law_comparison[law] = {
                        'description': data['description'],
                        'universal_traditions': data['traditions'],
                        'found_in_database': list(tradition_applications.keys()),
                        'total_applications': len(law_docs),
                        'tradition_applications': dict(tradition_applications)
                    }
        
        return law_comparison
    
    def get_symbol_context(self, text, symbol):
        """Extract context around symbol mentions"""
        text_lower = text.lower()
        symbol_lower = symbol.lower()
        
        # Find sentences containing the symbol
        sentences = re.split(r'[.!?]+', text)
        context_sentences = []
        
        for sentence in sentences:
            if symbol_lower in sentence.lower():
                context_sentences.append(sentence.strip())
        
        return context_sentences[:3]  # Return up to 3 contextual sentences
    
    def get_law_context(self, text, law):
        """Extract context around spiritual law applications"""
        # Convert law to readable terms
        law_terms = law.replace('law_of_', '').replace('_', ' ')
        
        # Look for related concepts in text
        text_lower = text.lower()
        context_phrases = []
        
        # Split into phrases and look for law-related content
        phrases = re.split(r'[.!?;]+', text)
        
        for phrase in phrases:
            phrase_lower = phrase.lower()
            if (law_terms in phrase_lower or 
                any(term in phrase_lower for term in law_terms.split())):
                context_phrases.append(phrase.strip())
        
        return context_phrases[:2]  # Return up to 2 contextual phrases
    
    def get_element_context(self, text, element):
        """Get context for any element (symbol, law, theme)"""
        element_lower = element.replace('_', ' ').lower()
        
        # Find paragraphs containing the element
        paragraphs = text.split('\n\n')
        relevant_paragraphs = []
        
        for para in paragraphs:
            if element_lower in para.lower():
                # Truncate long paragraphs
                if len(para) > 300:
                    para = para[:300] + "..."
                relevant_paragraphs.append(para.strip())
        
        return relevant_paragraphs[:2]  # Return up to 2 relevant paragraphs
    
    def advanced_forensic_search(self, query_type, query_value, filters=None):
        """Advanced search with multiple filter types"""
        
        if query_type == 'symbol':
            base_results = self.search_by_symbol(query_value)
        elif query_type == 'law':
            base_results = self.search_by_spiritual_law(query_value)
        elif query_type == 'theme':
            base_results = self.search_by_theme(query_value)
        elif query_type == 'verse':
            return self.search_by_verse_reference(query_value)
        else:
            return []
        
        # Apply additional filters if provided
        if filters:
            filtered_results = []
            
            for result in base_results:
                metadata = result['metadata']
                
                # Check tradition filter
                if 'tradition' in filters:
                    if metadata.get('tradition', '').lower() != filters['tradition'].lower():
                        continue
                
                # Check period filter
                if 'period' in filters:
                    if metadata.get('period', '').lower() != filters['period'].lower():
                        continue
                
                # Check symbol filter
                if 'has_symbol' in filters:
                    if filters['has_symbol'] not in metadata.get('symbols', []):
                        continue
                
                # Check law filter
                if 'has_law' in filters:
                    if filters['has_law'] not in metadata.get('spiritual_laws', []):
                        continue
                
                filtered_results.append(result)
            
            return filtered_results
        
        return base_results
    
    def interactive_forensic_search(self):
        """Interactive forensic search interface"""
        print("🔬 Divine Mirror AI - Spiritual Forensics Search Engine")
        print("=" * 60)
        print("Search by symbol, spiritual law, theme, or verse reference")
        print("Commands: 'symbol', 'law', 'theme', 'verse', 'compare', 'universal', 'help', 'quit'")
        
        while True:
            try:
                command = input("\n🔬 Forensic Search: ").strip().lower()
                
                if not command:
                    continue
                elif command in ['quit', 'exit', 'q']:
                    print("Investigation complete.")
                    break
                elif command == 'help':
                    self.show_forensic_help()
                elif command == 'symbol':
                    self.handle_symbol_search()
                elif command == 'law':
                    self.handle_law_search()
                elif command == 'theme':
                    self.handle_theme_search()
                elif command == 'verse':
                    self.handle_verse_search()
                elif command == 'compare':
                    self.handle_comparison_search()
                elif command == 'universal':
                    self.handle_universal_analysis()
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nInvestigation terminated.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_symbol_search(self):
        """Handle symbol search queries"""
        print("\n🔣 Available symbols:")
        symbols = list(self.forensic_stats.get('symbols', {}).keys())[:15]
        for i, symbol in enumerate(symbols, 1):
            count = self.forensic_stats['symbols'][symbol]
            print(f"   {i}. {symbol}: {count} occurrences")
        
        symbol = input("\nEnter symbol name: ").strip().lower()
        
        if symbol:
            results = self.search_by_symbol(symbol)
            
            print(f"\n🔍 Symbol Analysis: '{symbol}'")
            print(f"Found in {len(results)} documents")
            
            if symbol in self.symbol_dictionary:
                meanings = self.symbol_dictionary[symbol]['meanings']
                traditions = self.symbol_dictionary[symbol]['traditions']
                print(f"Universal meanings: {', '.join(meanings)}")
                print(f"Found in traditions: {', '.join(traditions)}")
            
            for i, result in enumerate(results[:5], 1):
                metadata = result['metadata']
                print(f"\n{i}. [{metadata['tradition']}] {metadata['title']}")
                print(f"   Context: {result['symbol_context'][0] if result['symbol_context'] else 'No specific context'}")
                print(f"   Related symbols: {', '.join(result['related_symbols'])}")
    
    def handle_law_search(self):
        """Handle spiritual law search queries"""
        print("\n⚖️ Available spiritual laws:")
        laws = list(self.forensic_stats.get('spiritual_laws', {}).keys())[:10]
        for i, law in enumerate(laws, 1):
            count = self.forensic_stats['spiritual_laws'][law]
            law_display = law.replace('_', ' ').title()
            print(f"   {i}. {law_display}: {count} occurrences")
        
        law = input("\nEnter spiritual law: ").strip().lower().replace(' ', '_')
        if not law.startswith('law_of_'):
            law = f"law_of_{law}"
        
        if law:
            results = self.search_by_spiritual_law(law)
            
            print(f"\n⚖️ Spiritual Law Analysis: '{law.replace('_', ' ').title()}'")
            print(f"Found in {len(results)} documents")
            
            if law in self.spiritual_laws:
                description = self.spiritual_laws[law]['description']
                traditions = self.spiritual_laws[law]['traditions']
                print(f"Description: {description}")
                print(f"Universal in: {', '.join(traditions)}")
            
            for i, result in enumerate(results[:5], 1):
                metadata = result['metadata']
                print(f"\n{i}. [{result['tradition']}] {metadata['title']}")
                print(f"   Application: {result['law_context'][0] if result['law_context'] else 'General application'}")
                print(f"   Related laws: {', '.join(result['related_laws'])}")
    
    def handle_theme_search(self):
        """Handle theme search queries"""
        print("\n🎭 Available themes:")
        themes = list(self.forensic_stats.get('themes', {}).keys())[:15]
        for i, theme in enumerate(themes, 1):
            count = self.forensic_stats['themes'][theme]
            theme_display = theme.replace('_', ' ').title()
            print(f"   {i}. {theme_display}: {count} occurrences")
        
        theme = input("\nEnter theme: ").strip().lower().replace(' ', '_')
        
        if theme:
            results = self.search_by_theme(theme)
            
            print(f"\n🎭 Theme Analysis: '{theme.replace('_', ' ').title()}'")
            print(f"Found in {len(results)} documents")
            
            for i, result in enumerate(results[:5], 1):
                metadata = result['metadata']
                print(f"\n{i}. [{metadata['tradition']}] {metadata['title']}")
                print(f"   Primary themes: {', '.join(result['primary_themes'])}")
                print(f"   Symbols: {', '.join(result['symbols_present'])}")
                print(f"   Laws: {', '.join(result['laws_present'])}")
    
    def handle_verse_search(self):
        """Handle verse reference search"""
        print("\n📖 Verse Reference Search")
        print("Examples: 'Genesis 1:1', 'John 3:16', 'Bhagavad Gita 2.47', 'Dhammapada 1'")
        
        verse_ref = input("\nEnter verse reference: ").strip()
        
        if verse_ref:
            results = self.search_by_verse_reference(verse_ref)
            
            print(f"\n📖 Verse Search Results: '{verse_ref}'")
            print(f"Found {len(results)} matching verses")
            
            for i, result in enumerate(results[:5], 1):
                print(f"\n{i}. {result['verse_reference']}")
                print(f"   Source: [{result['tradition']}] {result['source']} ({result['period']})")
                print(f"   Text: {result['verse_text']}")
    
    def handle_comparison_search(self):
        """Handle cross-tradition comparison"""
        print("\n🌍 Cross-Tradition Comparison")
        print("Compare symbols, laws, or themes across traditions")
        
        element_type = input("Element type (symbol/law/theme): ").strip().lower()
        element_name = input("Element name: ").strip().lower()
        
        if element_type and element_name:
            comparison = self.forensic_comparison(element_type, element_name)
            
            print(f"\n🌍 Cross-Tradition Analysis: {element_name}")
            print(f"Found in {comparison['traditions_found']} traditions")
            
            for tradition, items in comparison['tradition_breakdown'].items():
                print(f"\n🔹 {tradition}: {len(items)} occurrences")
                for item in items[:2]:  # Show first 2 per tradition
                    print(f"   📖 {item['source']}: {item['excerpt'][:100]}...")
    
    def handle_universal_analysis(self):
        """Handle universal archetype analysis"""
        print("\n🌟 Universal Archetype Analysis")
        print("Analyzing symbols found across 3+ traditions...")
        
        analysis = self.universal_archetype_analysis()
        
        print(f"Found {len(analysis)} universal symbols:")
        
        for symbol, data in list(analysis.items())[:5]:
            print(f"\n🔣 {symbol.title()}")
            print(f"   Meanings: {', '.join(data['universal_meanings'])}")
            print(f"   Traditions: {', '.join(data['traditions_with_symbol'])}")
            print(f"   Total occurrences: {data['total_occurrences']}")
    
    def show_forensic_help(self):
        """Show help for forensic search"""
        print("\n🔬 Spiritual Forensics Help:")
        print("   symbol     - Search by spiritual symbol (serpent, tree, water, etc.)")
        print("   law        - Search by spiritual law (karma, love, sacrifice, etc.)")
        print("   theme      - Search by spiritual theme (creation, redemption, etc.)")
        print("   verse      - Search for specific verse references")
        print("   compare    - Compare elements across traditions")
        print("   universal  - Analyze universal archetypes")
        print("   help       - Show this help")
        print("   quit       - Exit forensic search")

def main():
    """Main function"""
    engine = SpiritualForensicsEngine()
    
    if engine.documents:
        engine.interactive_forensic_search()
    else:
        print("No forensic database found. Please run divine_metadata_generator.py first.")

if __name__ == "__main__":
    main()