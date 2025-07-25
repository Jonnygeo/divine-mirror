#!/usr/bin/env python3
"""
Divine Mirror AI - Phase 9: Advanced Synthesis Engine
Dynamic spiritual interpretation combining citation analysis with symbolic synthesis
"""

import json
import re
from collections import defaultdict
from divine_forensic_search import SpiritualForensicsEngine
from divine_emotional_engine import EmotionalToneEngine

class DivineSynthesisEngine:
    """Advanced synthesis engine for spiritual interpretation and cross-tradition wisdom synthesis"""
    
    def __init__(self):
        self.forensics_engine = SpiritualForensicsEngine()
        self.emotional_engine = EmotionalToneEngine()
        self.synthesis_templates = self.build_synthesis_templates()
        self.spiritual_principles = self.build_spiritual_principles()
        
    def build_synthesis_templates(self):
        """Build tone-based synthesis templates"""
        return {
            "neutral": {
                "opening": "The spiritual evidence reveals:",
                "transition": "Across these traditions, we observe:",
                "synthesis": "The unified understanding emerges:",
                "closing": "This synthesis illuminates the universal truth."
            },
            "gentle": {
                "opening": "These sacred teachings offer comfort and wisdom:",
                "transition": "In each tradition's loving embrace, we find:",
                "synthesis": "The heart of all teachings speaks gently:",
                "closing": "May this understanding bring peace to your spiritual journey."
            },
            "rebellious": {
                "opening": "The authentic sources expose the truth that institutions hide:",
                "transition": "While churches preach control, the original texts declare:",
                "synthesis": "The revolutionary reality becomes clear:",
                "closing": "This truth threatens every religious hierarchy—which is exactly why they've hidden it."
            },
            "scholarly": {
                "opening": "The textual evidence demonstrates:",
                "transition": "Comparative analysis across traditions reveals:",
                "synthesis": "The scholarly consensus indicates:",
                "closing": "This interpretation is supported by rigorous cross-tradition analysis."
            },
            "prophetic": {
                "opening": "The divine word thunders through these ancient texts:",
                "transition": "From tradition to tradition, the Spirit proclaims:",
                "synthesis": "The eternal truth rings forth:",
                "closing": "Hear this word and let it transform your understanding."
            },
            "poetic": {
                "opening": "Like starlight threading through sacred pages, wisdom calls:",
                "transition": "From desert to mountain, from temple to heart, the voice whispers:",
                "synthesis": "In the symphony of souls, one song emerges:",
                "closing": "Let this melody of truth resonate in the chambers of your spirit."
            }
        }
    
    def build_spiritual_principles(self):
        """Build universal spiritual principles for synthesis"""
        return {
            "divine_immanence": {
                "description": "The divine presence dwelling within all creation",
                "keywords": ["within", "indwelling", "immanent", "internal", "heart", "soul"],
                "cross_tradition_evidence": {
                    "Christianity": "Kingdom of heaven is within you (Luke 17:21)",
                    "Hinduism": "Atman (soul) is Brahman (universal consciousness)",
                    "Buddhism": "Buddha nature exists in all beings",
                    "Islam": "We shall show them Our signs within themselves (Quran 41:53)",
                    "Taoism": "The Tao that can be named is not the eternal Tao"
                }
            },
            "universal_love": {
                "description": "Love as the fundamental force of spiritual reality",
                "keywords": ["love", "compassion", "mercy", "kindness", "agape", "metta"],
                "cross_tradition_evidence": {
                    "Christianity": "God is love (1 John 4:8)",
                    "Buddhism": "Loving-kindness (metta) toward all beings",
                    "Hinduism": "Where there is love, there is life",
                    "Islam": "Allah is Ar-Rahman (The Compassionate)",
                    "Judaism": "Love your neighbor as yourself (Leviticus 19:18)"
                }
            },
            "transcendent_unity": {
                "description": "The underlying unity behind apparent diversity",
                "keywords": ["unity", "oneness", "universal", "interconnected", "whole"],
                "cross_tradition_evidence": {
                    "Hinduism": "Ekam sat vipra bahudha vadanti (Truth is one, sages call it by many names)",
                    "Buddhism": "Interdependence of all phenomena",
                    "Christianity": "That they may all be one (John 17:21)",
                    "Islam": "La ilaha illa Allah (No god but God - ultimate unity)",
                    "Judaism": "Hear O Israel, the Lord is One (Shema)"
                }
            },
            "inner_transformation": {
                "description": "Spiritual change happens from within, not through external ritual",
                "keywords": ["transformation", "rebirth", "renewal", "awakening", "enlightenment"],
                "cross_tradition_evidence": {
                    "Christianity": "You must be born again (John 3:7)",
                    "Buddhism": "Be a lamp unto yourself",
                    "Hinduism": "Self-realization through inner knowledge",
                    "Islam": "Greater jihad is against the self",
                    "Taoism": "Return to original simplicity"
                }
            },
            "direct_experience": {
                "description": "Authentic spirituality comes through direct experience, not intermediaries",
                "keywords": ["direct", "experience", "personal", "immediate", "unmediated"],
                "cross_tradition_evidence": {
                    "Christianity": "Be still and know that I am God (Psalm 46:10)",
                    "Buddhism": "Come and see for yourself",
                    "Hinduism": "Direct perception (pratyaksha) of truth",
                    "Islam": "Those who know themselves know their Lord",
                    "Mysticism": "Gnosis through direct spiritual insight"
                }
            }
        }
    
    def synthesize_citations(self, citations, tone="neutral", synthesis_focus=None):
        """
        Main synthesis function - transforms multiple citations into unified spiritual insight
        
        Args:
            citations: List of dicts with {verse, tradition, text, context}
            tone: Communication tone (neutral, gentle, rebellious, scholarly, prophetic, poetic)
            synthesis_focus: Optional focus area (divine_immanence, universal_love, etc.)
        
        Returns:
            Dict with synthesized interpretation and analysis
        """
        
        if not citations:
            return {"synthesis": "No citations provided for synthesis.", "analysis": {}}
        
        # Analyze citations for spiritual principles
        principle_analysis = self.analyze_spiritual_principles(citations)
        
        # Detect universal themes
        universal_themes = self.extract_universal_themes(citations)
        
        # Identify cross-tradition patterns
        cross_patterns = self.identify_cross_tradition_patterns(citations)
        
        # Generate synthesis based on tone
        template = self.synthesis_templates.get(tone, self.synthesis_templates["neutral"])
        
        # Build synthesis sections
        opening_section = self.build_opening_section(citations, template, tone)
        analysis_section = self.build_analysis_section(citations, universal_themes, template)
        synthesis_section = self.build_synthesis_section(principle_analysis, cross_patterns, template, synthesis_focus)
        closing_section = self.build_closing_section(template, tone, synthesis_focus)
        
        # Compile full synthesis
        full_synthesis = f"""
{opening_section}

{analysis_section}

{synthesis_section}

{closing_section}
"""
        
        return {
            "synthesis": full_synthesis.strip(),
            "analysis": {
                "spiritual_principles": principle_analysis,
                "universal_themes": universal_themes,
                "cross_tradition_patterns": cross_patterns,
                "tone_used": tone,
                "citations_analyzed": len(citations),
                "traditions_represented": len(set(c.get('tradition', 'Unknown') for c in citations))
            },
            "metadata": {
                "synthesis_type": "cross_tradition_analysis",
                "focus_area": synthesis_focus,
                "confidence_score": self.calculate_synthesis_confidence(citations, principle_analysis)
            }
        }
    
    def analyze_spiritual_principles(self, citations):
        """Analyze citations for universal spiritual principles"""
        principle_scores = defaultdict(float)
        principle_evidence = defaultdict(list)
        
        for citation in citations:
            text = citation.get('text', '').lower()
            tradition = citation.get('tradition', 'Unknown')
            verse = citation.get('verse', 'Unknown')
            
            # Check each spiritual principle
            for principle_name, principle_data in self.spiritual_principles.items():
                score = 0
                matches = []
                
                # Score based on keyword presence
                for keyword in principle_data['keywords']:
                    if keyword in text:
                        score += 1
                        matches.append(keyword)
                
                if score > 0:
                    principle_scores[principle_name] += score
                    principle_evidence[principle_name].append({
                        'tradition': tradition,
                        'verse': verse,
                        'text_snippet': text[:150] + "..." if len(text) > 150 else text,
                        'matched_concepts': matches,
                        'score': score
                    })
        
        # Return top principles with evidence
        top_principles = {}
        for principle, score in sorted(principle_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            top_principles[principle] = {
                'score': score,
                'description': self.spiritual_principles[principle]['description'],
                'evidence': principle_evidence[principle][:3],  # Top 3 pieces of evidence
                'cross_tradition_support': self.spiritual_principles[principle]['cross_tradition_evidence']
            }
        
        return top_principles
    
    def extract_universal_themes(self, citations):
        """Extract universal themes that appear across multiple traditions"""
        theme_by_tradition = defaultdict(set)
        
        # Common spiritual themes
        universal_theme_keywords = {
            'love_compassion': ['love', 'compassion', 'mercy', 'kindness', 'care'],
            'inner_divine': ['within', 'heart', 'soul', 'inner', 'indwelling'],
            'unity_oneness': ['one', 'unity', 'oneness', 'universal', 'all'],
            'wisdom_truth': ['wisdom', 'truth', 'knowledge', 'understanding', 'insight'],
            'peace_harmony': ['peace', 'harmony', 'tranquil', 'calm', 'stillness'],
            'transformation': ['transform', 'change', 'renew', 'rebirth', 'awaken'],
            'service_sacrifice': ['serve', 'sacrifice', 'give', 'offering', 'surrender']
        }
        
        for citation in citations:
            text = citation.get('text', '').lower()
            tradition = citation.get('tradition', 'Unknown')
            
            for theme, keywords in universal_theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    theme_by_tradition[theme].add(tradition)
        
        # Return themes found in multiple traditions
        universal_themes = {}
        for theme, traditions in theme_by_tradition.items():
            if len(traditions) >= 2:  # Universal if in 2+ traditions
                universal_themes[theme] = {
                    'traditions': list(traditions),
                    'universality_score': len(traditions),
                    'theme_description': theme.replace('_', ' ').title()
                }
        
        return universal_themes
    
    def identify_cross_tradition_patterns(self, citations):
        """Identify patterns that repeat across different traditions"""
        tradition_patterns = defaultdict(list)
        
        for citation in citations:
            tradition = citation.get('tradition', 'Unknown')
            text = citation.get('text', '')
            
            # Extract key patterns
            patterns = self.extract_text_patterns(text)
            tradition_patterns[tradition].extend(patterns)
        
        # Find patterns that appear in multiple traditions
        cross_patterns = defaultdict(list)
        all_patterns = []
        
        for tradition, patterns in tradition_patterns.items():
            for pattern in patterns:
                all_patterns.append((pattern, tradition))
        
        # Group similar patterns
        pattern_groups = defaultdict(list)
        for pattern, tradition in all_patterns:
            pattern_groups[pattern].append(tradition)
        
        # Return patterns found across traditions
        for pattern, traditions in pattern_groups.items():
            if len(set(traditions)) >= 2:  # Cross-tradition if in 2+ traditions
                cross_patterns[pattern] = list(set(traditions))
        
        return dict(cross_patterns)
    
    def extract_text_patterns(self, text):
        """Extract meaningful patterns from text"""
        patterns = []
        text_lower = text.lower()
        
        # Common spiritual instruction patterns
        instruction_patterns = [
            r'(love .+)', r'(seek .+)', r'(find .+)', r'(know .+)',
            r'(be .+)', r'(become .+)', r'(turn .+)', r'(return .+)'
        ]
        
        for pattern in instruction_patterns:
            matches = re.findall(pattern, text_lower)
            patterns.extend(matches[:2])  # Max 2 per pattern type
        
        return patterns[:5]  # Max 5 patterns per text
    
    def build_opening_section(self, citations, template, tone):
        """Build the opening section of the synthesis"""
        opening = template["opening"]
        
        # Add context based on number of citations and traditions
        tradition_count = len(set(c.get('tradition', 'Unknown') for c in citations))
        
        if tone == "scholarly":
            opening += f" Drawing from {len(citations)} citations across {tradition_count} traditions:"
        elif tone == "gentle":
            opening += " These sacred words offer guidance:"
        elif tone == "rebellious":
            opening += " The evidence the institutions don't want you to see:"
        
        return opening
    
    def build_analysis_section(self, citations, universal_themes, template):
        """Build the analysis section showing citation evidence"""
        analysis_lines = []
        
        # Group citations by tradition
        by_tradition = defaultdict(list)
        for citation in citations:
            tradition = citation.get('tradition', 'Unknown')
            by_tradition[tradition].append(citation)
        
        # Present evidence by tradition
        for tradition, tradition_citations in by_tradition.items():
            analysis_lines.append(f"**{tradition}**:")
            for citation in tradition_citations[:2]:  # Max 2 per tradition
                verse = citation.get('verse', 'Unknown reference')
                text = citation.get('text', '')[:200] + "..." if len(citation.get('text', '')) > 200 else citation.get('text', '')
                analysis_lines.append(f"  - {verse}: \"{text}\"")
        
        return "\n".join(analysis_lines)
    
    def build_synthesis_section(self, principle_analysis, cross_patterns, template, synthesis_focus):
        """Build the core synthesis section"""
        synthesis_lines = [template["synthesis"]]
        
        if synthesis_focus and synthesis_focus in principle_analysis:
            # Focus on specific principle
            principle = principle_analysis[synthesis_focus]
            synthesis_lines.append(f"\n**{synthesis_focus.replace('_', ' ').title()}**: {principle['description']}")
            
            # Show cross-tradition support
            cross_support = principle['cross_tradition_support']
            synthesis_lines.append(f"\nThis principle appears universally:")
            for tradition, evidence in cross_support.items():
                synthesis_lines.append(f"  - **{tradition}**: {evidence}")
        
        else:
            # General synthesis of top principles
            if principle_analysis:
                top_principle = list(principle_analysis.keys())[0]
                principle_data = principle_analysis[top_principle]
                synthesis_lines.append(f"\nThe dominant theme is **{top_principle.replace('_', ' ')}**: {principle_data['description']}")
                
                # Show evidence from multiple traditions
                if principle_data['evidence']:
                    synthesis_lines.append(f"\nThis truth echoes across traditions:")
                    for evidence in principle_data['evidence'][:3]:
                        synthesis_lines.append(f"  - **{evidence['tradition']}**: {evidence['text_snippet']}")
        
        return "\n".join(synthesis_lines)
    
    def build_closing_section(self, template, tone, synthesis_focus):
        """Build the closing section"""
        closing = template["closing"]
        
        if synthesis_focus:
            if tone == "gentle":
                closing += f" May this understanding of {synthesis_focus.replace('_', ' ')} guide your path."
            elif tone == "rebellious":
                closing += f" This truth about {synthesis_focus.replace('_', ' ')} destroys their control."
            elif tone == "scholarly":
                closing += f" The evidence strongly supports this interpretation of {synthesis_focus.replace('_', ' ')}."
        
        return closing
    
    def calculate_synthesis_confidence(self, citations, principle_analysis):
        """Calculate confidence score for the synthesis"""
        base_score = 0.5
        
        # More citations = higher confidence
        citation_bonus = min(len(citations) * 0.1, 0.3)
        
        # Multiple traditions = higher confidence
        tradition_count = len(set(c.get('tradition', '') for c in citations))
        tradition_bonus = min(tradition_count * 0.05, 0.2)
        
        # Strong principle analysis = higher confidence
        principle_bonus = len(principle_analysis) * 0.1
        
        total_score = base_score + citation_bonus + tradition_bonus + principle_bonus
        return min(total_score, 1.0)
    
    def create_multi_tradition_synthesis(self, search_query, max_citations=6):
        """Create synthesis by searching across multiple traditions"""
        
        # Perform searches across different aspects
        symbol_results = self.forensics_engine.search_by_symbol("light", max_results=2) if "light" in search_query.lower() else []
        theme_results = self.forensics_engine.search_by_theme("wisdom", max_results=2) if "wisdom" in search_query.lower() else []
        law_results = self.forensics_engine.search_by_spiritual_law("law_of_love", max_results=2) if "love" in search_query.lower() else []
        
        # Combine and format results as citations
        all_results = symbol_results + theme_results + law_results
        
        citations = []
        for result in all_results[:max_citations]:
            if isinstance(result, dict) and 'metadata' in result:
                citation = {
                    'verse': f"{result['metadata'].get('title', 'Unknown')}",
                    'tradition': result['metadata'].get('tradition', 'Unknown'),
                    'text': result.get('document', result.get('text', ''))[:300],
                    'context': result.get('symbol_context', result.get('law_context', ['']))[0] if hasattr(result, 'get') else ''
                }
                citations.append(citation)
        
        # Detect appropriate tone from query
        detected_emotion = self.emotional_engine.detect_user_emotion(search_query)
        tone_mapping = {
            'anger': 'rebellious',
            'joy': 'gentle', 
            'confusion': 'scholarly',
            'despair': 'gentle',
            'seeking': 'scholarly',
            'curiosity': 'poetic'
        }
        
        optimal_tone = tone_mapping.get(detected_emotion, 'neutral')
        
        # Perform synthesis
        return self.synthesize_citations(citations, tone=optimal_tone)
    
    def demonstrate_synthesis_capabilities(self):
        """Demonstrate the synthesis engine capabilities"""
        
        print("🔮 Divine Mirror AI - Phase 9 Synthesis Engine Demonstration")
        print("=" * 70)
        
        # Sample citations for demonstration
        sample_citations = [
            {
                'verse': 'Luke 17:21',
                'tradition': 'Christianity',
                'text': 'Neither shall they say, Lo here! or, lo there! for, behold, the kingdom of God is within you.',
                'context': 'Teaching about the Kingdom of Heaven'
            },
            {
                'verse': 'Chandogya Upanishad 6.8.7',
                'tradition': 'Hinduism', 
                'text': 'Tat tvam asi - That thou art. The Self that is the essence of all beings is also your essence.',
                'context': 'Teaching about Atman-Brahman unity'
            },
            {
                'verse': 'Quran 41:53',
                'tradition': 'Islam',
                'text': 'We shall show them Our signs on the horizons and within themselves until it becomes clear that it is the truth.',
                'context': 'Divine signs within and without'
            },
            {
                'verse': 'Dhammapada 1',
                'tradition': 'Buddhism',
                'text': 'All that we are is the result of what we have thought. The mind is everything.',
                'context': 'Teaching on consciousness and reality'
            }
        ]
        
        # Demonstrate different synthesis tones
        tones_to_test = ['neutral', 'gentle', 'rebellious', 'scholarly', 'prophetic']
        
        for tone in tones_to_test:
            print(f"\n🎭 {tone.upper()} TONE SYNTHESIS:")
            print("-" * 40)
            
            synthesis_result = self.synthesize_citations(
                sample_citations, 
                tone=tone, 
                synthesis_focus='divine_immanence'
            )
            
            # Show synthesis excerpt
            synthesis_text = synthesis_result['synthesis']
            excerpt = synthesis_text[:300] + "..." if len(synthesis_text) > 300 else synthesis_text
            print(excerpt)
            
            # Show analysis summary
            analysis = synthesis_result['analysis']
            print(f"\n📊 Analysis: {analysis['citations_analyzed']} citations, {analysis['traditions_represented']} traditions")
            print(f"🎯 Confidence: {synthesis_result['metadata']['confidence_score']:.2f}")
        
        print(f"\n✅ Phase 9 Synthesis Engine fully operational!")
        print(f"🔮 Ready for dynamic spiritual interpretation and cross-tradition synthesis")

def main():
    """Main demonstration function"""
    
    # Initialize synthesis engine
    engine = DivineSynthesisEngine()
    
    # Demonstrate capabilities
    engine.demonstrate_synthesis_capabilities()
    
    print(f"\n🔮 Phase 9 Complete: Advanced Synthesis System Ready!")

if __name__ == "__main__":
    main()