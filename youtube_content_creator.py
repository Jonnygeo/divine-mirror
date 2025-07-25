#!/usr/bin/env python3
"""
Divine Mirror AI - YouTube Content Creation Tool
Generate evidence-based content for truth-seeking video series
"""

import json
import re
from collections import defaultdict
from divine_cross_comparison import CrossTextComparator
from divine_advanced_search import AdvancedSearchEngine

class YouTubeContentCreator:
    """Content creation tool for truth-seeking YouTube series"""
    
    def __init__(self):
        self.comparator = CrossTextComparator()
        self.search_engine = AdvancedSearchEngine()
        
        # Pre-defined series topics
        self.series_topics = {
            "yeshua_vs_jesus": {
                "title": "Yeshua vs Jesus: Reclaiming the Original Name",
                "tags": ["jesus_yeshua", "divine_nature", "institutional_authority"],
                "manipulation_focus": ["authority_control", "fear_based"]
            },
            "kingdom_within": {
                "title": "The Kingdom Within: Original Teaching vs External Church",
                "tags": ["kingdom_heaven", "direct_experience", "inner"],
                "manipulation_focus": ["institutional_authority", "power_control"]
            },
            "hell_doctrine": {
                "title": "Hell: Fear-Based Control vs Original Afterlife Teachings",
                "tags": ["hell_punishment", "fear_based", "afterlife"],
                "manipulation_focus": ["fear_control", "guilt_shame"]
            },
            "sacred_feminine": {
                "title": "The Sacred Feminine: Suppressed Divine Wisdom",
                "tags": ["sacred_feminine", "divine_nature", "wisdom_knowledge"],
                "manipulation_focus": ["authority_control", "power_control"]
            },
            "money_changers": {
                "title": "Money Changers: Wealth vs Spiritual Poverty",
                "tags": ["wealth_poverty", "material_focus", "social_justice"],
                "manipulation_focus": ["material_focus", "power_control"]
            }
        }
    
    def generate_episode_outline(self, topic_key):
        """Generate comprehensive episode outline with evidence"""
        
        if topic_key not in self.series_topics:
            return None
        
        topic = self.series_topics[topic_key]
        
        outline = {
            "title": topic["title"],
            "hook": self.generate_hook(topic_key),
            "introduction": self.generate_introduction(topic_key),
            "evidence_sections": self.gather_evidence_sections(topic),
            "manipulation_analysis": self.analyze_manipulation_patterns(topic),
            "cross_tradition_comparison": self.compare_across_traditions(topic),
            "conclusion": self.generate_conclusion(topic_key),
            "call_to_action": self.generate_call_to_action(topic_key),
            "citations": []
        }
        
        return outline
    
    def generate_hook(self, topic_key):
        """Generate compelling opening hooks"""
        
        hooks = {
            "yeshua_vs_jesus": [
                "What if I told you that 'Jesus' isn't even his real name?",
                "The name that could unlock the real teachings has been hidden for 2000 years.",
                "Every time you say 'Jesus,' you're speaking a Roman creation, not the Hebrew teacher."
            ],
            "kingdom_within": [
                "Yeshua said the Kingdom of Heaven is within you. So why do churches insist you need them to access it?",
                "What if the most revolutionary teaching was deliberately buried by those who profit from your dependence?",
                "The original message threatens every religious institution on Earth."
            ],
            "hell_doctrine": [
                "Hell as eternal torture? That's not in the original texts.",
                "The word 'hell' appears 54 times in the King James Bible. Here's what it actually meant.",
                "Fear-based control through mistranslation: How 'Sheol' became 'eternal damnation.'"
            ],
            "sacred_feminine": [
                "They erased half of the divine. Here's the evidence.",
                "The sacred feminine was systematically removed from Christianity. Let me show you the proof.",
                "Mary Magdalene wasn't a prostitute. That lie was invented to suppress her real role."
            ],
            "money_changers": [
                "Yeshua's only violent act was against the money system. Churches today are the money changers.",
                "He lived in poverty and taught spiritual wealth. Modern Christianity preaches prosperity gospel.",
                "The man who said 'sell everything and give to the poor' is now used to justify mega-church wealth."
            ]
        }
        
        return hooks.get(topic_key, ["Truth seekers, prepare to have your reality shattered."])
    
    def generate_introduction(self, topic_key):
        """Generate episode introductions"""
        
        intros = {
            "yeshua_vs_jesus": "Today we're diving deep into the original Hebrew name and teachings that have been systematically obscured by institutional Christianity. Using 164 sacred texts across 17 religious traditions, we'll uncover what the historical figure actually taught versus what modern churches claim.",
            
            "kingdom_within": "The most revolutionary teaching in human history has been buried under layers of institutional control. Today we examine Yeshua's core message about the Kingdom Within and how religious authorities have redirected this internal spiritual truth toward external dependence on their systems.",
            
            "hell_doctrine": "Fear has been the primary tool of religious control for centuries. Today we trace the evolution of afterlife teachings from their original Hebrew context through Greek translation errors to modern fire-and-brimstone manipulation. The evidence will shock you.",
            
            "sacred_feminine": "Half of the divine nature has been systematically erased from Christianity. Today we recover the suppressed teachings about divine feminine wisdom, the real Mary Magdalene, and how patriarchal institutions rewrote spiritual history to eliminate feminine authority.",
            
            "money_changers": "The man who lived in complete poverty and violently opposed the money system is now used to justify mega-church wealth and prosperity gospel. Today we examine this fundamental contradiction and trace how spiritual teachings became economic manipulation."
        }
        
        return intros.get(topic_key, "Today we examine one of the most suppressed truths in religious history.")
    
    def gather_evidence_sections(self, topic):
        """Gather evidence from the sacred text database"""
        
        evidence_sections = []
        
        # Search for each topic tag
        for tag in topic["tags"]:
            results = self.search_engine.search_by_tags([tag], max_results=5)
            
            if results:
                section = {
                    "concept": tag.replace('_', ' ').title(),
                    "evidence": []
                }
                
                for doc in results:
                    evidence_item = {
                        "tradition": doc['metadata'].get('tradition', 'Unknown'),
                        "source": doc['metadata'].get('title', 'Unknown'),
                        "period": doc['metadata'].get('period', 'Unknown'),
                        "text": doc['text'][:200] + "...",
                        "significance": self.analyze_significance(doc, tag)
                    }
                    section["evidence"].append(evidence_item)
                
                evidence_sections.append(section)
        
        return evidence_sections
    
    def analyze_manipulation_patterns(self, topic):
        """Analyze manipulation patterns relevant to topic"""
        
        manipulation_analysis = []
        
        for pattern in topic["manipulation_focus"]:
            pattern_docs = self.search_engine.search_by_tags([pattern], max_results=3)
            
            if pattern_docs:
                analysis = {
                    "pattern_type": pattern.replace('_', ' ').title(),
                    "description": self.get_pattern_description(pattern),
                    "examples": []
                }
                
                for doc in pattern_docs:
                    example = {
                        "source": doc['metadata'].get('title', 'Unknown'),
                        "tradition": doc['metadata'].get('tradition', 'Unknown'),
                        "manipulation_text": doc['text'][:150] + "...",
                        "analysis": self.analyze_manipulation_technique(doc, pattern)
                    }
                    analysis["examples"].append(example)
                
                manipulation_analysis.append(analysis)
        
        return manipulation_analysis
    
    def compare_across_traditions(self, topic):
        """Compare topic across different religious traditions"""
        
        comparison = {
            "universal_themes": [],
            "tradition_specific": [],
            "institutional_variations": []
        }
        
        # Find how different traditions handle the same concepts
        for tag in topic["tags"]:
            cross_analysis = self.comparator.analyze_concept_across_traditions(tag)
            
            if cross_analysis:
                universal_theme = {
                    "concept": tag.replace('_', ' ').title(),
                    "traditions_found": cross_analysis['traditions_found'],
                    "common_elements": self.extract_common_elements(cross_analysis),
                    "variations": self.extract_variations(cross_analysis)
                }
                comparison["universal_themes"].append(universal_theme)
        
        return comparison
    
    def generate_conclusion(self, topic_key):
        """Generate episode conclusions"""
        
        conclusions = {
            "yeshua_vs_jesus": "The evidence is clear: the original Hebrew teacher's name, message, and methods have been systematically altered to serve institutional power. When we return to the source materials, we find a revolutionary spiritual teacher whose authentic message threatens every religious hierarchy.",
            
            "kingdom_within": "Yeshua's core teaching about the Kingdom Within directly contradicts every external religious authority. This isn't coincidence—it's deliberate suppression of the most liberating spiritual truth ever taught. You don't need intermediaries for divine connection.",
            
            "hell_doctrine": "The hell doctrine is revealed as mistranslation, cultural projection, and deliberate fear-mongering. Original texts show a radically different understanding of afterlife that emphasizes love, restoration, and universal spiritual evolution rather than eternal punishment.",
            
            "sacred_feminine": "The systematic erasure of divine feminine wisdom represents one of history's greatest spiritual crimes. Recovering these teachings restores balance and reveals the complete divine nature that patriarchal institutions have hidden.",
            
            "money_changers": "Modern prosperity gospel and mega-church wealth represent the exact system Yeshua violently opposed. His teachings about spiritual wealth versus material accumulation have been inverted to justify the very corruption he condemned."
        }
        
        return conclusions.get(topic_key, "The evidence demands we question everything we've been taught and return to authentic spiritual truth.")
    
    def generate_call_to_action(self, topic_key):
        """Generate episode call-to-action"""
        
        return "Don't take my word for it. Use the Divine Mirror AI to search these texts yourself. Verify every claim. The truth can withstand scrutiny—manipulation cannot. Links to all sources in the description. Share this video if it opened your eyes, and subscribe for more evidence-based truth analysis."
    
    def analyze_significance(self, doc, tag):
        """Analyze why a document is significant for a topic"""
        
        significance_map = {
            "jesus_yeshua": "Shows original Hebrew context vs later Greek/Roman interpretations",
            "kingdom_heaven": "Reveals internal spiritual focus vs external institutional dependence",
            "hell_punishment": "Demonstrates mistranslation of original Sheol/Hades concepts",
            "sacred_feminine": "Preserves suppressed feminine divine wisdom",
            "material_focus": "Exposes contradiction between spiritual and material priorities"
        }
        
        return significance_map.get(tag, "Provides authentic textual evidence for analysis")
    
    def get_pattern_description(self, pattern):
        """Get description of manipulation patterns"""
        
        descriptions = {
            "fear_based": "Uses terror, threat, and intimidation to control behavior",
            "authority_control": "Demands unquestioning obedience to religious hierarchy",
            "material_focus": "Redirects spiritual teachings toward material accumulation",
            "guilt_shame": "Induces psychological shame to maintain dependence",
            "power_control": "Concentrates spiritual authority in institutional leaders"
        }
        
        return descriptions.get(pattern, "Systematic manipulation technique")
    
    def analyze_manipulation_technique(self, doc, pattern):
        """Analyze specific manipulation techniques in text"""
        
        return f"This passage demonstrates {pattern.replace('_', ' ')} by emphasizing external authority over internal spiritual development, typical of institutional control mechanisms."
    
    def extract_common_elements(self, cross_analysis):
        """Extract common elements across traditions"""
        
        return ["Universal spiritual principles", "Inner divine connection", "Ethical moral framework"]
    
    def extract_variations(self, cross_analysis):
        """Extract variations between traditions"""
        
        return ["Cultural expressions differ", "Ritual practices vary", "Institutional interpretations diverge"]
    
    def create_episode_script(self, topic_key):
        """Generate complete episode script"""
        
        outline = self.generate_episode_outline(topic_key)
        
        if not outline:
            return "Topic not found"
        
        script = f"""
# {outline['title']}

## HOOK (0:00-0:30)
{outline['hook'][0]}

## INTRODUCTION (0:30-1:30)
{outline['introduction']}

## EVIDENCE SECTIONS (1:30-8:00)
"""
        
        for section in outline['evidence_sections']:
            script += f"\n### {section['concept']} Evidence\n"
            for evidence in section['evidence'][:2]:  # Top 2 pieces of evidence
                script += f"- **{evidence['tradition']} ({evidence['period']})**: {evidence['text']}\n"
                script += f"  *Significance*: {evidence['significance']}\n\n"
        
        script += "\n## MANIPULATION ANALYSIS (8:00-10:00)\n"
        for analysis in outline['manipulation_analysis']:
            script += f"\n### {analysis['pattern_type']}\n"
            script += f"{analysis['description']}\n"
            for example in analysis['examples'][:1]:  # One example per pattern
                script += f"- **Example**: {example['manipulation_text']}\n"
                script += f"  *Analysis*: {example['analysis']}\n\n"
        
        script += f"\n## CONCLUSION (10:00-11:00)\n{outline['conclusion']}\n"
        script += f"\n## CALL TO ACTION (11:00-11:30)\n{outline['call_to_action']}\n"
        
        return script

def main():
    """Demo the content creator"""
    creator = YouTubeContentCreator()
    
    print("🎬 Divine Mirror AI - YouTube Content Creator")
    print("=" * 50)
    
    # Generate content for all series topics
    for topic_key in creator.series_topics.keys():
        print(f"\n📽️ Generating content for: {creator.series_topics[topic_key]['title']}")
        
        outline = creator.generate_episode_outline(topic_key)
        
        if outline:
            print(f"✅ Hook: {outline['hook'][0]}")
            print(f"✅ Evidence sections: {len(outline['evidence_sections'])}")
            print(f"✅ Manipulation patterns: {len(outline['manipulation_analysis'])}")
            
            # Save script
            script = creator.create_episode_script(topic_key)
            with open(f"episode_{topic_key}_script.md", 'w', encoding='utf-8') as f:
                f.write(script)
            print(f"💾 Script saved: episode_{topic_key}_script.md")

if __name__ == "__main__":
    main()