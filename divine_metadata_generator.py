#!/usr/bin/env python3
"""
Divine Mirror AI - Phase 7: Advanced Metadata Generator
Creates comprehensive metadata for spiritual forensics and symbolic analysis
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

class SpiritualMetadataGenerator:
    """Generate advanced metadata for spiritual texts with symbols, laws, and themes"""
    
    def __init__(self, enhanced_index_file="divine_enhanced_index.json"):
        self.load_enhanced_index(enhanced_index_file)
        self.symbol_dictionary = self.build_symbol_dictionary()
        self.spiritual_laws = self.build_spiritual_laws()
        self.verse_patterns = self.build_verse_patterns()
        
    def load_enhanced_index(self, filename):
        """Load the enhanced index"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.documents = data['documents']
            self.metadata_index = data['metadata_index']
            print(f"✅ Loaded {len(self.documents)} documents for metadata generation")
        except FileNotFoundError:
            print("❌ Enhanced index not found")
            self.documents = []
    
    def build_symbol_dictionary(self):
        """Build comprehensive symbol dictionary across traditions"""
        return {
            # Universal Symbols
            "serpent": {
                "meanings": ["wisdom", "temptation", "transformation", "healing", "kundalini"],
                "traditions": ["Christianity", "Hinduism", "Buddhism", "Egyptian", "Greek"]
            },
            "tree": {
                "meanings": ["life", "knowledge", "axis_mundi", "growth", "connection"],
                "traditions": ["Christianity", "Judaism", "Norse", "Celtic", "Hinduism"]
            },
            "water": {
                "meanings": ["purification", "life", "consciousness", "baptism", "flow"],
                "traditions": ["Christianity", "Hinduism", "Taoism", "Buddhism", "Islam"]
            },
            "fire": {
                "meanings": ["purification", "divine_presence", "destruction", "passion", "illumination"],
                "traditions": ["Christianity", "Zoroastrianism", "Hinduism", "Greek", "Norse"]
            },
            "mountain": {
                "meanings": ["divine_dwelling", "ascension", "stability", "revelation", "meditation"],
                "traditions": ["Christianity", "Buddhism", "Hinduism", "Greek", "Taoism"]
            },
            "dove": {
                "meanings": ["peace", "holy_spirit", "divine_messenger", "purity", "love"],
                "traditions": ["Christianity", "Judaism", "Islam", "Greek", "Roman"]
            },
            "lion": {
                "meanings": ["courage", "divine_power", "royalty", "solar_energy", "strength"],
                "traditions": ["Christianity", "Judaism", "Hinduism", "Egyptian", "Buddhism"]
            },
            "eagle": {
                "meanings": ["divine_vision", "spiritual_ascension", "power", "freedom", "messenger"],
                "traditions": ["Christianity", "Native_American", "Greek", "Roman", "Germanic"]
            },
            "lotus": {
                "meanings": ["purity", "enlightenment", "rebirth", "beauty", "transcendence"],
                "traditions": ["Hinduism", "Buddhism", "Egyptian", "Greek", "Jainism"]
            },
            "cross": {
                "meanings": ["sacrifice", "intersection", "balance", "suffering", "redemption"],
                "traditions": ["Christianity", "Celtic", "Egyptian", "Hindu", "Buddhist"]
            },
            "circle": {
                "meanings": ["wholeness", "eternity", "unity", "perfection", "cycles"],
                "traditions": ["Christianity", "Buddhism", "Hinduism", "Celtic", "Native_American"]
            },
            "light": {
                "meanings": ["divine_presence", "knowledge", "truth", "consciousness", "revelation"],
                "traditions": ["Christianity", "Islam", "Hinduism", "Buddhism", "Gnosticism"]
            },
            "darkness": {
                "meanings": ["mystery", "unconscious", "evil", "potential", "void"],
                "traditions": ["Christianity", "Gnosticism", "Hinduism", "Buddhism", "Kabbalah"]
            },
            "bridge": {
                "meanings": ["connection", "transition", "mediation", "journey", "rainbow_bridge"],
                "traditions": ["Christianity", "Norse", "Hinduism", "Buddhism", "Shamanism"]
            },
            "bread": {
                "meanings": ["sustenance", "communion", "life", "sharing", "divine_provision"],
                "traditions": ["Christianity", "Judaism", "Islam", "Egyptian", "Greek"]
            },
            "wine": {
                "meanings": ["transformation", "divine_blood", "celebration", "intoxication", "sacrifice"],
                "traditions": ["Christianity", "Greek", "Roman", "Persian", "Egyptian"]
            }
        }
    
    def build_spiritual_laws(self):
        """Build spiritual laws dictionary"""
        return {
            "law_of_attraction": {
                "description": "Like attracts like; thoughts manifest reality",
                "traditions": ["Hinduism", "Buddhism", "Christianity", "Hermetic", "New_Thought"]
            },
            "law_of_karma": {
                "description": "Action and consequence; moral causation",
                "traditions": ["Hinduism", "Buddhism", "Jainism", "Sikhism", "Theosophy"]
            },
            "law_of_sacrifice": {
                "description": "Giving up lesser for greater; spiritual exchange",
                "traditions": ["Christianity", "Judaism", "Islam", "Hinduism", "Buddhism"]
            },
            "law_of_love": {
                "description": "Love as fundamental force and commandment",
                "traditions": ["Christianity", "Sufism", "Hinduism", "Buddhism", "Bahai"]
            },
            "law_of_non_resistance": {
                "description": "Non-violent response to opposition; turning other cheek",
                "traditions": ["Christianity", "Buddhism", "Jainism", "Hinduism", "Taoism"]
            },
            "law_of_divine_unity": {
                "description": "All is One; interconnectedness of existence",
                "traditions": ["Hinduism", "Buddhism", "Sufism", "Kabbalah", "Hermeticism"]
            },
            "law_of_reciprocity": {
                "description": "Golden Rule; treat others as you wish to be treated",
                "traditions": ["Christianity", "Judaism", "Islam", "Buddhism", "Hinduism"]
            },
            "law_of_detachment": {
                "description": "Freedom from attachment to outcomes",
                "traditions": ["Buddhism", "Hinduism", "Taoism", "Christianity", "Sufism"]
            },
            "law_of_correspondence": {
                "description": "As above, so below; microcosm reflects macrocosm",
                "traditions": ["Hermeticism", "Kabbalah", "Hinduism", "Gnosticism", "Alchemy"]
            },
            "law_of_forgiveness": {
                "description": "Release of resentment; spiritual cleansing",
                "traditions": ["Christianity", "Buddhism", "Judaism", "Islam", "Hinduism"]
            }
        }
    
    def build_verse_patterns(self):
        """Build patterns for verse recognition"""
        return {
            "biblical": r"(\d?\s?[A-Za-z]+)\s+(\d+):(\d+)",  # "Genesis 1:1" or "1 Kings 2:3"
            "quran": r"(Quran|Qur'an|Sura|Surah)\s+(\d+):(\d+)",  # "Quran 2:255"
            "bhagavad_gita": r"(Bhagavad\s+Gita|BG)\s+(\d+)\.(\d+)",  # "Bhagavad Gita 2.47"
            "dhammapada": r"(Dhammapada|DHP)\s+(\d+)",  # "Dhammapada 1"
            "tao_te_ching": r"(Tao\s+Te\s+Ching|TTC)\s+(\d+)",  # "Tao Te Ching 1"
            "upanishads": r"([A-Za-z]+\s+Upanishad)\s+(\d+)\.(\d+)",  # "Isha Upanishad 1.1"
        }
    
    def detect_symbols(self, text):
        """Detect symbols in text content"""
        text_lower = text.lower()
        detected_symbols = []
        
        for symbol, data in self.symbol_dictionary.items():
            # Look for symbol name and related terms
            symbol_terms = [symbol] + [meaning.replace('_', ' ') for meaning in data['meanings']]
            
            for term in symbol_terms:
                if term in text_lower:
                    detected_symbols.append(symbol)
                    break
        
        return list(set(detected_symbols))
    
    def detect_spiritual_laws(self, text):
        """Detect spiritual laws in text content"""
        text_lower = text.lower()
        detected_laws = []
        
        # Key phrases that indicate spiritual laws
        law_indicators = {
            "law_of_karma": ["karma", "reap what you sow", "action consequence", "deed result"],
            "law_of_love": ["love one another", "greatest commandment", "love thy neighbor", "divine love"],
            "law_of_sacrifice": ["sacrifice", "give up", "offering", "surrender", "lay down life"],
            "law_of_attraction": ["ask and receive", "seek and find", "faith moves mountains"],
            "law_of_reciprocity": ["golden rule", "do unto others", "treat others"],
            "law_of_forgiveness": ["forgive", "mercy", "pardon", "release"],
            "law_of_non_resistance": ["turn other cheek", "resist not evil", "non-violence"],
            "law_of_divine_unity": ["all is one", "unity", "oneness", "interconnected"],
            "law_of_detachment": ["detachment", "let go", "non-attachment", "surrender outcome"],
            "law_of_correspondence": ["as above so below", "reflect", "correspondence", "microcosm"]
        }
        
        for law, indicators in law_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    detected_laws.append(law)
                    break
        
        return list(set(detected_laws))
    
    def extract_verses(self, text, tradition):
        """Extract verse references from text"""
        verses = {}
        
        # Split text into lines and look for verse-like patterns
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Look for biblical verse patterns
            if tradition == "Christianity":
                # Look for chapter:verse patterns
                verse_match = re.search(r'(\d+):(\d+)', line_stripped)
                if verse_match and len(line_stripped) > 20:  # Ensure it's substantial content
                    chapter, verse = verse_match.groups()
                    key = f"{chapter}:{verse}"
                    verses[key] = line_stripped[:200] + "..." if len(line_stripped) > 200 else line_stripped
            
            # Look for numbered verses in other traditions
            elif tradition in ["Buddhism", "Hinduism", "Taoism"]:
                # Look for numbered sections
                if re.match(r'^\d+\.', line_stripped) and len(line_stripped) > 15:
                    verse_num = re.match(r'^(\d+)\.', line_stripped).group(1)
                    verses[verse_num] = line_stripped[:200] + "..." if len(line_stripped) > 200 else line_stripped
        
        # Limit to top 10 verses per document
        return dict(list(verses.items())[:10])
    
    def determine_themes(self, text, symbols, laws, tradition):
        """Determine spiritual themes based on content analysis"""
        text_lower = text.lower()
        themes = []
        
        # Theme detection based on content and context
        theme_keywords = {
            "creation": ["creation", "beginning", "genesis", "origin", "first"],
            "redemption": ["redemption", "salvation", "saved", "rescue", "deliver"],
            "enlightenment": ["enlightenment", "awakening", "realization", "insight", "understanding"],
            "suffering": ["suffering", "pain", "affliction", "tribulation", "anguish"],
            "liberation": ["liberation", "freedom", "moksha", "nirvana", "release"],
            "divine_union": ["union", "oneness", "unity", "communion", "connection"],
            "moral_law": ["commandment", "law", "rule", "moral", "ethical"],
            "death_rebirth": ["death", "rebirth", "resurrection", "reincarnation", "renewal"],
            "wisdom": ["wisdom", "knowledge", "understanding", "insight", "truth"],
            "compassion": ["compassion", "mercy", "kindness", "love", "care"],
            "justice": ["justice", "righteousness", "fair", "judgment", "equity"],
            "faith": ["faith", "belief", "trust", "confidence", "devotion"],
            "prayer": ["prayer", "meditation", "worship", "devotion", "contemplation"],
            "community": ["community", "fellowship", "brotherhood", "sisterhood", "gathering"],
            "pilgrimage": ["journey", "pilgrimage", "path", "way", "quest"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)
        
        # Add themes based on detected symbols and laws
        if "serpent" in symbols:
            themes.extend(["temptation", "wisdom", "transformation"])
        if "tree" in symbols:
            themes.extend(["life", "knowledge", "growth"])
        if "law_of_karma" in laws:
            themes.append("moral_causation")
        if "law_of_love" in laws:
            themes.append("divine_love")
        
        return list(set(themes))
    
    def find_cross_tradition_links(self, symbols, laws, themes, tradition):
        """Find cross-tradition connections"""
        cross_links = {}
        
        # Find traditions that share symbols
        for symbol in symbols:
            if symbol in self.symbol_dictionary:
                related_traditions = self.symbol_dictionary[symbol]['traditions']
                for related_tradition in related_traditions:
                    if related_tradition != tradition:
                        if related_tradition not in cross_links:
                            cross_links[related_tradition] = []
                        cross_links[related_tradition].append(f"symbol: {symbol}")
        
        # Find traditions that share spiritual laws
        for law in laws:
            if law in self.spiritual_laws:
                related_traditions = self.spiritual_laws[law]['traditions']
                for related_tradition in related_traditions:
                    if related_tradition != tradition:
                        if related_tradition not in cross_links:
                            cross_links[related_tradition] = []
                        cross_links[related_tradition].append(f"law: {law}")
        
        return cross_links
    
    def generate_document_metadata(self, doc):
        """Generate comprehensive metadata for a document"""
        text = doc['text']
        metadata = doc['metadata']
        tradition = metadata.get('tradition', 'Unknown')
        
        # Detect symbols, laws, and themes
        symbols = self.detect_symbols(text)
        laws = self.detect_spiritual_laws(text)
        themes = self.determine_themes(text, symbols, laws, tradition)
        verses = self.extract_verses(text, tradition)
        cross_links = self.find_cross_tradition_links(symbols, laws, themes, tradition)
        
        # Enhanced metadata structure
        enhanced_metadata = {
            **metadata,  # Preserve existing metadata
            "symbols": symbols,
            "spiritual_laws": laws,
            "themes": themes,
            "key_verses": verses,
            "cross_tradition_links": cross_links,
            "symbol_count": len(symbols),
            "law_count": len(laws),
            "theme_count": len(themes),
            "verse_count": len(verses),
            "forensic_signature": {
                "primary_symbols": symbols[:3],
                "primary_laws": laws[:2],
                "primary_themes": themes[:3]
            }
        }
        
        return enhanced_metadata
    
    def process_all_documents(self):
        """Process all documents and generate enhanced metadata"""
        print("🔬 Divine Mirror AI - Spiritual Forensics Metadata Generator")
        print("=" * 65)
        
        enhanced_documents = []
        
        # Statistics tracking
        all_symbols = defaultdict(int)
        all_laws = defaultdict(int)
        all_themes = defaultdict(int)
        cross_tradition_stats = defaultdict(int)
        
        for i, doc in enumerate(self.documents):
            try:
                enhanced_metadata = self.generate_document_metadata(doc)
                
                # Create enhanced document
                enhanced_doc = {
                    **doc,
                    'metadata': enhanced_metadata
                }
                enhanced_documents.append(enhanced_doc)
                
                # Update statistics
                for symbol in enhanced_metadata['symbols']:
                    all_symbols[symbol] += 1
                
                for law in enhanced_metadata['spiritual_laws']:
                    all_laws[law] += 1
                
                for theme in enhanced_metadata['themes']:
                    all_themes[theme] += 1
                
                for tradition in enhanced_metadata['cross_tradition_links']:
                    cross_tradition_stats[tradition] += 1
                
                if (i + 1) % 100 == 0:
                    print(f"⏱️ Processed {i + 1}/{len(self.documents)} documents")
                    
            except Exception as e:
                print(f"⚠️ Error processing document {i}: {e}")
                enhanced_documents.append(doc)  # Keep original if processing fails
        
        # Create comprehensive forensic index
        forensic_index = {
            'documents': enhanced_documents,
            'metadata_index': {doc['id']: doc['metadata'] for doc in enhanced_documents},
            'word_index': {},  # Would need to rebuild from enhanced docs
            'forensic_statistics': {
                'symbols': dict(sorted(all_symbols.items(), key=lambda x: x[1], reverse=True)),
                'spiritual_laws': dict(sorted(all_laws.items(), key=lambda x: x[1], reverse=True)),
                'themes': dict(sorted(all_themes.items(), key=lambda x: x[1], reverse=True)),
                'cross_tradition_connections': dict(sorted(cross_tradition_stats.items(), key=lambda x: x[1], reverse=True))
            },
            'symbol_dictionary': self.symbol_dictionary,
            'spiritual_laws_reference': self.spiritual_laws
        }
        
        # Save enhanced forensic index
        with open("divine_forensic_index.json", 'w', encoding='utf-8') as f:
            json.dump(forensic_index, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎯 Spiritual Forensics Metadata Complete!")
        print(f"✅ Documents processed: {len(enhanced_documents)}")
        print(f"🔍 Unique symbols detected: {len(all_symbols)}")
        print(f"⚖️ Spiritual laws identified: {len(all_laws)}")
        print(f"🎭 Themes catalogued: {len(all_themes)}")
        print(f"🌐 Cross-tradition links: {len(cross_tradition_stats)}")
        print(f"💾 Forensic index saved: divine_forensic_index.json")
        
        # Display top findings
        print(f"\n🔝 Top 10 Universal Symbols:")
        for symbol, count in list(all_symbols.items())[:10]:
            print(f"   {symbol}: {count} occurrences")
        
        print(f"\n⚖️ Top 10 Spiritual Laws:")
        for law, count in list(all_laws.items())[:10]:
            print(f"   {law.replace('_', ' ').title()}: {count} occurrences")
        
        print(f"\n🎭 Top 10 Themes:")
        for theme, count in list(all_themes.items())[:10]:
            print(f"   {theme.replace('_', ' ').title()}: {count} occurrences")
        
        return forensic_index

def main():
    """Main execution function"""
    generator = SpiritualMetadataGenerator()
    
    if not generator.documents:
        print("No documents found. Run divine_intelligent_tagger.py first.")
        return
    
    # Generate comprehensive spiritual forensics metadata
    forensic_index = generator.process_all_documents()
    
    print(f"\n🔬 Phase 7 Complete: Spiritual Forensics System Ready!")
    print(f"Your Divine Mirror AI can now search by symbol, spiritual law, theme, and verse.")

if __name__ == "__main__":
    main()