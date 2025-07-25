#!/usr/bin/env python3
"""
Divine Mirror AI - Phase 5: Intelligent Tagging System
Adds semantic tags and cross-religious comparison capabilities
"""

import os
import json
import re
from collections import defaultdict, Counter
from pathlib import Path

class IntelligentTagger:
    """Advanced tagging system for sacred texts"""
    
    def __init__(self, index_file="divine_text_index.json"):
        self.load_index(index_file)
        self.concept_keywords = self.build_concept_dictionary()
        
    def load_index(self, filename):
        """Load the text index"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data['documents']
            self.metadata_index = data['metadata_index']
            self.word_index = {word: set(doc_ids) for word, doc_ids in data['word_index'].items()}
            self.stats = data['stats']
            
            print(f"✅ Loaded {len(self.documents)} documents for tagging")
            
        except FileNotFoundError:
            print("❌ Index file not found. Run divine_simple_processor.py first.")
            self.documents = []
    
    def build_concept_dictionary(self):
        """Build dictionary of spiritual/religious concepts and their keywords"""
        return {
            # Core Spiritual Concepts
            "divine_nature": ["god", "divine", "allah", "brahman", "tao", "buddha", "consciousness", "spirit", "holy", "sacred"],
            "salvation_liberation": ["salvation", "liberation", "moksha", "nirvana", "enlightenment", "redemption", "deliverance", "freedom"],
            "love_compassion": ["love", "compassion", "mercy", "kindness", "forgiveness", "grace", "charity", "benevolence"],
            "wisdom_knowledge": ["wisdom", "knowledge", "understanding", "truth", "gnosis", "insight", "awareness", "revelation"],
            "prayer_meditation": ["prayer", "meditation", "contemplation", "worship", "devotion", "mindfulness", "silence"],
            
            # Afterlife Concepts
            "heaven_paradise": ["heaven", "paradise", "celestial", "eternal", "blessed", "glory", "resurrection"],
            "hell_punishment": ["hell", "punishment", "damnation", "fire", "torment", "gehenna", "sheol", "underworld"],
            "soul_spirit": ["soul", "spirit", "atman", "consciousness", "essence", "inner", "heart", "mind"],
            
            # Religious Authority
            "institutional_authority": ["church", "priest", "rabbi", "imam", "authority", "hierarchy", "institution", "clergy"],
            "direct_experience": ["within", "inner", "personal", "direct", "mystical", "experience", "union", "communion"],
            "scripture_text": ["scripture", "text", "word", "teaching", "doctrine", "law", "commandment", "verse"],
            
            # Ethical Teachings
            "morality_ethics": ["righteousness", "virtue", "ethics", "morality", "justice", "good", "evil", "sin"],
            "peace_harmony": ["peace", "harmony", "balance", "tranquility", "serenity", "calm", "stillness"],
            "suffering_pain": ["suffering", "pain", "affliction", "tribulation", "sorrow", "grief", "anguish"],
            
            # Social Justice
            "social_justice": ["justice", "oppression", "poor", "rich", "equality", "fairness", "widow", "orphan"],
            "wealth_poverty": ["wealth", "money", "riches", "poverty", "treasure", "gold", "silver", "material"],
            "power_control": ["power", "control", "dominion", "authority", "rule", "command", "subjugation"],
            
            # Mystical Concepts
            "unity_oneness": ["unity", "oneness", "union", "connection", "wholeness", "integration", "non-dual"],
            "transformation": ["transformation", "rebirth", "renewal", "change", "conversion", "awakening"],
            "sacred_feminine": ["feminine", "mother", "goddess", "sophia", "shakti", "mary", "maiden", "crone"],
            
            # Manipulation Indicators
            "fear_control": ["fear", "afraid", "terror", "dread", "intimidation", "threat", "coercion"],
            "guilt_shame": ["guilt", "shame", "condemnation", "unworthiness", "disgrace", "humiliation"],
            "obedience_submission": ["obey", "submit", "surrender", "compliance", "subjection", "servitude"]
        }
    
    def extract_concepts(self, text):
        """Extract spiritual concepts from text using keyword matching"""
        text_lower = text.lower()
        concepts = []
        
        for concept, keywords in self.concept_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches >= 2:  # Require at least 2 keyword matches
                concepts.append((concept, matches))
        
        # Sort by relevance and return top concepts
        concepts.sort(key=lambda x: x[1], reverse=True)
        return [concept for concept, score in concepts[:5]]
    
    def detect_tradition_themes(self, text, tradition):
        """Detect tradition-specific themes"""
        text_lower = text.lower()
        themes = []
        
        if tradition == "Christianity":
            christian_themes = {
                "jesus_yeshua": ["jesus", "yeshua", "christ", "messiah", "son"],
                "kingdom_heaven": ["kingdom", "heaven", "eternal", "life"],
                "trinity": ["father", "son", "spirit", "trinity"],
                "crucifixion": ["cross", "crucify", "death", "sacrifice"],
                "resurrection": ["risen", "resurrection", "life", "death"]
            }
            for theme, keywords in christian_themes.items():
                if sum(1 for k in keywords if k in text_lower) >= 2:
                    themes.append(theme)
        
        elif tradition == "Buddhism":
            buddhist_themes = {
                "four_truths": ["suffering", "desire", "cessation", "path"],
                "dharma": ["dharma", "teaching", "law", "truth"],
                "karma": ["karma", "action", "consequence", "rebirth"],
                "meditation": ["meditation", "mindfulness", "awareness", "concentration"]
            }
            for theme, keywords in buddhist_themes.items():
                if sum(1 for k in keywords if k in text_lower) >= 2:
                    themes.append(theme)
        
        elif tradition == "Islam":
            islamic_themes = {
                "allah": ["allah", "god", "divine", "creator"],
                "prophet": ["prophet", "muhammad", "messenger"],
                "quran": ["quran", "revelation", "book", "guidance"],
                "hajj": ["pilgrimage", "mecca", "hajj", "journey"]
            }
            for theme, keywords in islamic_themes.items():
                if sum(1 for k in keywords if k in text_lower) >= 2:
                    themes.append(theme)
        
        elif tradition == "Hinduism":
            hindu_themes = {
                "dharma": ["dharma", "duty", "righteousness", "law"],
                "karma": ["karma", "action", "consequence", "deed"],
                "moksha": ["moksha", "liberation", "freedom", "release"],
                "brahman": ["brahman", "absolute", "reality", "consciousness"]
            }
            for theme, keywords in hindu_themes.items():
                if sum(1 for k in keywords if k in text_lower) >= 2:
                    themes.append(theme)
        
        elif tradition == "Taoism":
            taoist_themes = {
                "tao": ["tao", "way", "path", "nature"],
                "wu_wei": ["action", "effort", "natural", "flow"],
                "yin_yang": ["balance", "harmony", "opposite", "complement"],
                "virtue": ["virtue", "goodness", "simplicity", "humility"]
            }
            for theme, keywords in taoist_themes.items():
                if sum(1 for k in keywords if k in text_lower) >= 2:
                    themes.append(theme)
        
        return themes
    
    def tag_document(self, doc):
        """Generate comprehensive tags for a document"""
        text = doc['text']
        metadata = doc['metadata']
        tradition = metadata.get('tradition', 'Unknown')
        
        # Extract general spiritual concepts
        concepts = self.extract_concepts(text)
        
        # Extract tradition-specific themes
        themes = self.detect_tradition_themes(text, tradition)
        
        # Detect manipulation indicators
        manipulation_indicators = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["fear", "afraid", "terror", "punishment"]):
            manipulation_indicators.append("fear_based")
        
        if any(word in text_lower for word in ["obey", "submit", "authority", "hierarchy"]):
            manipulation_indicators.append("authority_control")
        
        if any(word in text_lower for word in ["money", "wealth", "gold", "silver", "treasure"]):
            manipulation_indicators.append("material_focus")
        
        # Create comprehensive tag set
        all_tags = concepts + themes + manipulation_indicators
        
        # Add metadata-based tags
        all_tags.append(f"tradition_{tradition.lower()}")
        all_tags.append(f"period_{metadata.get('period', 'unknown').lower()}")
        all_tags.append(f"type_{metadata.get('type', 'unknown').lower()}")
        
        return list(set(all_tags))  # Remove duplicates
    
    def tag_all_documents(self):
        """Tag all documents in the collection"""
        print("🏷️ Divine Mirror AI - Intelligent Tagging System")
        print("=" * 55)
        
        tagged_documents = []
        tag_statistics = Counter()
        
        for i, doc in enumerate(self.documents):
            tags = self.tag_document(doc)
            
            # Update document with tags
            enhanced_doc = doc.copy()
            enhanced_doc['metadata']['tags'] = tags
            enhanced_doc['metadata']['tag_count'] = len(tags)
            
            tagged_documents.append(enhanced_doc)
            
            # Update statistics
            for tag in tags:
                tag_statistics[tag] += 1
            
            if (i + 1) % 100 == 0:
                print(f"⏱️ Tagged {i + 1}/{len(self.documents)} documents")
        
        # Save enhanced index
        enhanced_index = {
            'documents': tagged_documents,
            'metadata_index': {doc['id']: doc['metadata'] for doc in tagged_documents},
            'word_index': {word: list(doc_ids) for word, doc_ids in self.word_index.items()},
            'stats': self.stats,
            'tag_statistics': dict(tag_statistics.most_common(50))
        }
        
        with open("divine_enhanced_index.json", 'w', encoding='utf-8') as f:
            json.dump(enhanced_index, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Tagging Complete!")
        print(f"✅ Documents tagged: {len(tagged_documents)}")
        print(f"🏷️ Unique tags: {len(tag_statistics)}")
        print(f"💾 Enhanced index saved: divine_enhanced_index.json")
        
        # Show top tags
        print(f"\n🔝 Top 15 Concepts Identified:")
        for tag, count in tag_statistics.most_common(15):
            print(f"   {tag}: {count} documents")
        
        return enhanced_index
    
    def analyze_cross_tradition_themes(self, enhanced_index):
        """Analyze themes across different religious traditions"""
        print(f"\n🌍 Cross-Tradition Theme Analysis")
        print("=" * 40)
        
        tradition_themes = defaultdict(lambda: defaultdict(int))
        
        for doc in enhanced_index['documents']:
            tradition = doc['metadata'].get('tradition', 'Unknown')
            tags = doc['metadata'].get('tags', [])
            
            # Count concept tags (exclude metadata tags)
            concept_tags = [tag for tag in tags if not tag.startswith(('tradition_', 'period_', 'type_'))]
            
            for tag in concept_tags:
                tradition_themes[tradition][tag] += 1
        
        # Find universal themes (present in multiple traditions)
        all_themes = set()
        for tradition_data in tradition_themes.values():
            all_themes.update(tradition_data.keys())
        
        universal_themes = []
        for theme in all_themes:
            traditions_with_theme = sum(1 for t_data in tradition_themes.values() 
                                      if theme in t_data and t_data[theme] > 0)
            if traditions_with_theme >= 3:  # Present in at least 3 traditions
                total_count = sum(t_data.get(theme, 0) for t_data in tradition_themes.values())
                universal_themes.append((theme, traditions_with_theme, total_count))
        
        universal_themes.sort(key=lambda x: x[2], reverse=True)
        
        print("🌟 Universal Spiritual Themes (Found in 3+ Traditions):")
        for theme, tradition_count, total_count in universal_themes[:10]:
            print(f"   {theme}: {tradition_count} traditions, {total_count} documents")
        
        return tradition_themes

def main():
    """Main execution function"""
    tagger = IntelligentTagger()
    
    if not tagger.documents:
        print("No documents found. Run divine_simple_processor.py first.")
        return
    
    # Tag all documents
    enhanced_index = tagger.tag_all_documents()
    
    # Analyze cross-tradition themes
    tagger.analyze_cross_tradition_themes(enhanced_index)
    
    print(f"\n🎯 Phase 5 Complete: Intelligent Tagging System Ready!")
    print(f"Enhanced search now available with semantic tags and cross-tradition analysis.")

if __name__ == "__main__":
    main()