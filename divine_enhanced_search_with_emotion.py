#!/usr/bin/env python3
"""
Divine Mirror AI - Enhanced Search with Emotional Intelligence
Combines forensic search capabilities with emotional tone adaptation
"""

import json
from divine_forensic_search import SpiritualForensicsEngine
from divine_emotional_engine import EmotionalToneEngine

class EmotionallyAwareSearch:
    """Enhanced search engine with emotional intelligence and tone adaptation"""
    
    def __init__(self):
        self.forensics_engine = SpiritualForensicsEngine()
        self.emotional_engine = EmotionalToneEngine()
        
    def emotionally_aware_search(self, user_query, search_type='theme'):
        """Perform search with emotional context awareness"""
        
        # Analyze user's emotional state
        emotional_context = self.emotional_engine.create_emotional_response_metadata(user_query)
        
        # Perform appropriate search based on detected emotion and query
        if search_type == 'symbol':
            # Extract symbol from query
            symbol = self.extract_search_term(user_query, 'symbol')
            results = self.forensics_engine.search_by_symbol(symbol)
        elif search_type == 'law':
            # Extract spiritual law from query
            law = self.extract_search_term(user_query, 'law')
            results = self.forensics_engine.search_by_spiritual_law(law)
        elif search_type == 'verse':
            # Extract verse reference
            verse = self.extract_search_term(user_query, 'verse')
            results = self.forensics_engine.search_by_verse_reference(verse)
        else:
            # Default theme search
            theme = self.extract_search_term(user_query, 'theme')
            results = self.forensics_engine.search_by_theme(theme)
        
        # Generate emotionally-aware response
        tone_adjusted_response = self.emotional_engine.generate_tone_adjusted_prompt(
            user_query, results, emotional_context
        )
        
        return {
            'search_results': results,
            'emotional_context': emotional_context,
            'response_guidance': tone_adjusted_response,
            'search_metadata': {
                'query': user_query,
                'search_type': search_type,
                'results_count': len(results),
                'detected_emotion': emotional_context['emotional_analysis']['primary_emotion'],
                'recommended_tone': emotional_context['emotional_analysis']['recommended_tone']
            }
        }
    
    def extract_search_term(self, query, search_type):
        """Extract relevant search terms from user query"""
        query_lower = query.lower()
        
        if search_type == 'symbol':
            # Common spiritual symbols
            symbols = ['serpent', 'tree', 'water', 'fire', 'light', 'dove', 'lion', 'eagle', 'lotus', 'cross']
            for symbol in symbols:
                if symbol in query_lower:
                    return symbol
            return 'light'  # Default symbol
        
        elif search_type == 'law':
            # Spiritual laws
            if 'karma' in query_lower:
                return 'law_of_karma'
            elif 'love' in query_lower:
                return 'law_of_love' 
            elif 'sacrifice' in query_lower:
                return 'law_of_sacrifice'
            elif 'forgiveness' in query_lower or 'forgive' in query_lower:
                return 'law_of_forgiveness'
            else:
                return 'law_of_love'  # Default law
        
        elif search_type == 'verse':
            # Look for verse patterns
            import re
            verse_patterns = [
                r'([A-Za-z]+\s+\d+:\d+)',  # "Genesis 1:1"
                r'(\d+\s+[A-Za-z]+\s+\d+:\d+)',  # "1 Kings 2:3"
                r'([A-Za-z]+\s+\d+\.\d+)',  # "Bhagavad Gita 2.47"
            ]
            
            for pattern in verse_patterns:
                match = re.search(pattern, query)
                if match:
                    return match.group(1)
            return 'Genesis 1:1'  # Default verse
        
        else:  # theme search
            # Common spiritual themes
            themes = ['creation', 'redemption', 'love', 'forgiveness', 'wisdom', 'justice', 'faith', 'compassion']
            for theme in themes:
                if theme in query_lower:
                    return theme
            return 'wisdom'  # Default theme
    
    def provide_emotionally_intelligent_guidance(self, user_query):
        """Provide comprehensive emotionally intelligent spiritual guidance"""
        
        # Detect query type and perform appropriate search
        query_type = self.detect_query_type(user_query)
        
        # Perform emotionally-aware search
        enhanced_results = self.emotionally_aware_search(user_query, query_type)
        
        # Format response based on emotional context
        formatted_response = self.format_emotional_response(enhanced_results)
        
        return formatted_response
    
    def detect_query_type(self, query):
        """Detect what type of search the user needs"""
        query_lower = query.lower()
        
        # Check for verse references
        import re
        if re.search(r'[A-Za-z]+\s+\d+:\d+', query) or re.search(r'\d+\s+[A-Za-z]+\s+\d+:\d+', query):
            return 'verse'
        
        # Check for symbol queries
        symbol_indicators = ['symbol', 'serpent', 'tree', 'water', 'fire', 'light', 'dove', 'lion', 'eagle']
        if any(indicator in query_lower for indicator in symbol_indicators):
            return 'symbol'
        
        # Check for spiritual law queries  
        law_indicators = ['law', 'karma', 'sacrifice', 'forgiveness', 'reciprocity', 'golden rule']
        if any(indicator in query_lower for indicator in law_indicators):
            return 'law'
        
        # Default to theme search
        return 'theme'
    
    def format_emotional_response(self, enhanced_results):
        """Format response based on emotional context"""
        
        emotional_context = enhanced_results['emotional_context']
        search_results = enhanced_results['search_results']
        response_guidance = enhanced_results['response_guidance']
        
        # Get emotional analysis
        emotion = emotional_context['emotional_analysis']['primary_emotion']
        tone = emotional_context['emotional_analysis']['recommended_tone']
        intensity = emotional_context['emotional_analysis']['spiritual_intensity']
        
        # Format based on detected emotion
        if emotion == 'anger':
            opening = "I understand your frustration with religious deception. Let's examine the authentic evidence:"
        elif emotion == 'despair':
            opening = "I hear the pain in your spiritual journey. Here's healing truth from the original sources:"
        elif emotion == 'confusion':
            opening = "Your questions deserve clear, evidence-based answers. Here's what the authentic texts reveal:"
        elif emotion == 'joy':
            opening = "I'm glad you're finding truth! Let's explore this discovery further:"
        elif emotion == 'curiosity':
            opening = "Your curiosity about spiritual truth is commendable. Here's what the research shows:"
        else:  # seeking
            opening = "Your search for authentic spirituality is important. Here's what the evidence reveals:"
        
        # Format search results
        formatted_results = []
        
        for i, result in enumerate(search_results[:3], 1):
            if isinstance(result, dict):
                if 'verse_reference' in result:  # Verse search result
                    formatted_results.append(f"""
**{i}. {result['verse_reference']}** - [{result['tradition']}] {result['source']}
*"{result['verse_text']}"*
""")
                elif 'metadata' in result:  # Symbol/Law/Theme search result
                    formatted_results.append(f"""
**{i}. [{result['metadata']['tradition']}] {result['metadata']['title']}**
{result['document']}
""")
        
        # Construct full response
        full_response = f"""
{opening}

## Search Results:
{''.join(formatted_results)}

## Emotional Context Analysis:
- **Detected Emotion**: {emotion.title()}
- **Spiritual Intensity**: {intensity}
- **Recommended Tone**: {tone.title()}
- **Response Strategy**: {emotional_context['response_strategy']['approach'].replace('_', ' ').title()}

## Guidance:
{response_guidance['prompt'].split('RESPONSE INSTRUCTIONS:')[1] if 'RESPONSE INSTRUCTIONS:' in response_guidance['prompt'] else 'Continue seeking truth with authentic sources.'}
"""
        
        return {
            'response': full_response,
            'metadata': enhanced_results['search_metadata'],
            'emotional_analysis': emotional_context
        }

def main():
    """Demo the emotionally-aware search system"""
    
    search_engine = EmotionallyAwareSearch()
    
    print("🎭 Divine Mirror AI - Emotionally Aware Search Demo")
    print("=" * 55)
    
    test_queries = [
        "I'm angry about church lies regarding hell doctrine!",
        "What does the serpent symbol really mean across traditions?", 
        "I'm confused about what Genesis 1:1 actually says in Hebrew",
        "Show me the law of forgiveness in different religions",
        "I'm seeking wisdom about Yeshua's authentic teachings"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: \"{query}\"")
        
        # Get emotionally intelligent response
        result = search_engine.provide_emotionally_intelligent_guidance(query)
        
        print(f"🎭 Emotion: {result['metadata']['detected_emotion']}")
        print(f"🎨 Tone: {result['metadata']['recommended_tone']}")
        print(f"🔍 Search Type: {result['metadata']['search_type']}")
        print(f"📊 Results: {result['metadata']['results_count']} matches")
        
        # Show snippet of response
        response_snippet = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
        print(f"💬 Response Preview: {response_snippet}")

if __name__ == "__main__":
    main()