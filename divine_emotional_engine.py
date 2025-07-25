#!/usr/bin/env python3
"""
Divine Mirror AI - Phase 8: Emotional Tone Engine
Adaptive emotional intelligence and tone-aware spiritual response synthesis
"""

import json
import re
from collections import defaultdict
from pathlib import Path

class EmotionalToneEngine:
    """Emotional intelligence and adaptive tone engine for spiritual responses"""
    
    def __init__(self):
        self.load_emotional_configurations()
        self.spiritual_tone_profiles = self.build_spiritual_tone_profiles()
        self.emotion_detection_patterns = self.build_emotion_patterns()
        
    def load_emotional_configurations(self):
        """Load emotion map and tone styles from Phase 8 files"""
        
        # Load emotion mapping
        try:
            emotion_map_path = Path("attached_assets/Phase_8_EmotionalToneEngine/emotion_models/emotion_map.json")
            with open(emotion_map_path, 'r', encoding='utf-8') as f:
                self.emotion_map = json.load(f)
        except FileNotFoundError:
            self.emotion_map = {
                "joy": ["gentle", "poetic"],
                "anger": ["rebel", "prophetic"],
                "confusion": ["scholarly", "gentle"],
                "seeking": ["scholarly", "poetic"],
                "despair": ["gentle", "prophetic"],
                "curiosity": ["scholarly", "poetic"],
                "frustration": ["rebel", "scholarly"],
                "yearning": ["poetic", "prophetic"]
            }
        
        # Load tone styles
        try:
            styles_path = Path("attached_assets/Phase_8_EmotionalToneEngine/tone_styles/styles.json")
            with open(styles_path, 'r', encoding='utf-8') as f:
                self.tone_styles = json.load(f)
        except FileNotFoundError:
            self.tone_styles = {
                "default": "neutral",
                "rebel": "Bold, confrontational truth",
                "scholarly": "Analytical and precise",
                "gentle": "Soft and comforting",
                "prophetic": "Heavy, warning, divine urgency",
                "poetic": "Rhythmic, emotionally charged language"
            }
        
        # Load response template
        try:
            template_path = Path("attached_assets/Phase_8_EmotionalToneEngine/prompt_templates/response_template.txt")
            with open(template_path, 'r', encoding='utf-8') as f:
                self.response_template = f.read().strip()
        except FileNotFoundError:
            self.response_template = "Respond in a {tone_style} tone with spiritual insight. Prioritize emotional resonance and authenticity."
        
        print(f"✅ Emotional Tone Engine loaded with {len(self.emotion_map)} emotion types and {len(self.tone_styles)} tone styles")
    
    def build_spiritual_tone_profiles(self):
        """Build enhanced spiritual tone profiles for Divine Mirror AI"""
        return {
            "truth_seeker": {
                "description": "Honest, direct spiritual inquiry focused on authentic truth",
                "tone_markers": ["analytical", "questioning", "evidence-based"],
                "response_style": "scholarly",
                "spiritual_approach": "investigative_wisdom"
            },
            "wounded_believer": {
                "description": "Hurt by religious institutions but seeking authentic spirituality",
                "tone_markers": ["betrayed", "cautious", "seeking healing"],
                "response_style": "gentle",
                "spiritual_approach": "healing_restoration"
            },
            "rebel_awakening": {
                "description": "Angry at religious deception, ready for radical truth",
                "tone_markers": ["anger", "rebellion", "confrontational"],
                "response_style": "rebel",
                "spiritual_approach": "prophetic_judgment"
            },
            "mystic_explorer": {
                "description": "Deep spiritual seeker exploring cross-tradition wisdom",
                "tone_markers": ["wonder", "contemplative", "transcendent"],
                "response_style": "poetic",
                "spiritual_approach": "mystical_synthesis"
            },
            "biblical_researcher": {
                "description": "Academic approach to biblical and religious text analysis",
                "tone_markers": ["scholarly", "precise", "evidence-focused"],
                "response_style": "scholarly",
                "spiritual_approach": "textual_forensics"
            },
            "prophetic_voice": {
                "description": "Called to expose religious corruption with divine urgency",
                "tone_markers": ["urgent", "warning", "divinely_appointed"],
                "response_style": "prophetic",
                "spiritual_approach": "divine_judgment"
            }
        }
    
    def build_emotion_patterns(self):
        """Build patterns for detecting user emotions from text"""
        return {
            "joy": {
                "keywords": ["happy", "blessed", "grateful", "wonderful", "amazing", "beautiful", "love this", "thank you"],
                "patterns": [r"thank\s+you", r"this\s+is\s+amazing", r"so\s+beautiful", r"blessed\s+to"]
            },
            "anger": {
                "keywords": ["angry", "furious", "hate", "disgusted", "sick of", "tired of", "lies", "manipulation", "corrupt"],
                "patterns": [r"sick\s+of", r"tired\s+of", r"can't\s+stand", r"makes\s+me\s+angry", r"fed\s+up"]
            },
            "confusion": {
                "keywords": ["confused", "don't understand", "unclear", "mixed up", "lost", "what does", "help me understand"],
                "patterns": [r"don't\s+understand", r"what\s+does\s+.+\s+mean", r"help\s+me", r"confused\s+about"]
            },
            "seeking": {
                "keywords": ["looking for", "searching", "seeking", "want to know", "tell me about", "explain", "show me"],
                "patterns": [r"looking\s+for", r"want\s+to\s+know", r"tell\s+me\s+about", r"show\s+me", r"explain"]
            },
            "despair": {
                "keywords": ["hopeless", "lost", "broken", "devastated", "crushed", "betrayed", "abandoned", "alone"],
                "patterns": [r"feel\s+hopeless", r"so\s+broken", r"been\s+betrayed", r"feel\s+abandoned"]
            },
            "curiosity": {
                "keywords": ["curious", "interesting", "wonder", "what if", "could it be", "fascinating", "intrigued"],
                "patterns": [r"what\s+if", r"could\s+it\s+be", r"i\s+wonder", r"curious\s+about"]
            },
            "frustration": {
                "keywords": ["frustrated", "stuck", "blocked", "can't find", "nothing works", "getting nowhere"],
                "patterns": [r"can't\s+find", r"nothing\s+works", r"getting\s+nowhere", r"so\s+frustrated"]
            },
            "yearning": {
                "keywords": ["longing", "yearning", "hungry for", "thirsty", "desperate for", "deeply want", "soul needs"],
                "patterns": [r"hungry\s+for", r"thirsty\s+for", r"desperate\s+for", r"soul\s+needs", r"deeply\s+want"]
            }
        }
    
    def detect_user_emotion(self, user_input):
        """Detect primary emotion from user input"""
        text_lower = user_input.lower()
        emotion_scores = defaultdict(float)
        
        # Check for emotional keywords and patterns
        for emotion, data in self.emotion_detection_patterns.items():
            # Score based on keywords
            for keyword in data['keywords']:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1.0
            
            # Score based on patterns (higher weight)
            for pattern in data['patterns']:
                matches = re.findall(pattern, text_lower)
                emotion_scores[emotion] += len(matches) * 1.5
        
        # Detect spiritual context modifiers
        spiritual_intensity = self.detect_spiritual_intensity(text_lower)
        if spiritual_intensity > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] *= (1 + spiritual_intensity * 0.3)
        
        # Return highest scoring emotion or default to 'seeking'
        if emotion_scores:
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
            return primary_emotion
        else:
            return 'seeking'  # Default for spiritual inquiry
    
    def detect_spiritual_intensity(self, text_lower):
        """Detect how spiritually intense the user's query is"""
        spiritual_markers = [
            "god", "jesus", "yeshua", "christ", "holy", "sacred", "divine", "spiritual", "soul", 
            "faith", "belief", "religion", "church", "bible", "scripture", "prayer", "worship",
            "truth", "wisdom", "enlightenment", "awakening", "consciousness", "transcendent"
        ]
        
        intensity_markers = [
            "deeply", "profoundly", "desperately", "urgently", "completely", "absolutely",
            "life-changing", "transformative", "revolutionary", "earth-shattering"
        ]
        
        spiritual_count = sum(1 for marker in spiritual_markers if marker in text_lower)
        intensity_count = sum(1 for marker in intensity_markers if marker in text_lower)
        
        return min((spiritual_count + intensity_count * 2) / 10, 1.0)  # Normalize to 0-1
    
    def determine_optimal_tone(self, emotion, spiritual_context=None):
        """Determine optimal response tone based on emotion and spiritual context"""
        
        # Get base tone options from emotion mapping
        if emotion in self.emotion_map:
            tone_options = self.emotion_map[emotion]
        else:
            tone_options = ["scholarly"]  # Default fallback
        
        # Apply spiritual context modifiers
        if spiritual_context:
            if "institutional_criticism" in spiritual_context:
                if "rebel" in tone_options:
                    return "rebel"  # Strong criticism needs rebellious tone
                else:
                    return "prophetic"  # Alternative strong tone
            
            elif "personal_healing" in spiritual_context:
                if "gentle" in tone_options:
                    return "gentle"  # Healing needs gentle approach
                else:
                    return "scholarly"  # Gentle scholarly approach
            
            elif "deep_mystery" in spiritual_context:
                if "poetic" in tone_options:
                    return "poetic"  # Mystical content needs poetic expression
                else:
                    return "scholarly"  # Academic mysticism
        
        # Return first available tone or default
        return tone_options[0] if tone_options else "scholarly"
    
    def analyze_spiritual_context(self, user_input):
        """Analyze what type of spiritual context the user is engaging with"""
        text_lower = user_input.lower()
        contexts = []
        
        # Institutional criticism context
        if any(word in text_lower for word in ["church", "pastor", "priest", "institution", "corrupt", "manipulation", "control", "lies"]):
            contexts.append("institutional_criticism")
        
        # Personal healing context
        if any(word in text_lower for word in ["hurt", "healing", "broken", "betrayed", "wounded", "recovery", "restore"]):
            contexts.append("personal_healing")
        
        # Deep mystery context
        if any(word in text_lower for word in ["mystery", "mystical", "transcendent", "consciousness", "enlightenment", "awakening", "divine"]):
            contexts.append("deep_mystery")
        
        # Truth seeking context
        if any(word in text_lower for word in ["truth", "authentic", "original", "real", "actual", "genuine", "evidence"]):
            contexts.append("truth_seeking")
        
        # Cross-tradition context
        if any(word in text_lower for word in ["hinduism", "buddhism", "islam", "taoism", "traditions", "religions", "compare"]):
            contexts.append("cross_tradition")
        
        return contexts
    
    def generate_tone_adjusted_prompt(self, user_query, search_results, base_analysis):
        """Generate emotionally-aware prompt for AI response"""
        
        # Detect user emotion and spiritual context
        emotion = self.detect_user_emotion(user_query)
        spiritual_contexts = self.analyze_spiritual_context(user_query) 
        optimal_tone = self.determine_optimal_tone(emotion, spiritual_contexts)
        
        # Get tone style description
        tone_style = self.tone_styles.get(optimal_tone, self.tone_styles["default"])
        
        # Build emotionally-aware prompt
        emotional_prompt = f"""
EMOTIONAL CONTEXT ANALYSIS:
- Detected User Emotion: {emotion}
- Spiritual Context: {', '.join(spiritual_contexts) if spiritual_contexts else 'general_inquiry'}
- Optimal Response Tone: {optimal_tone}
- Tone Style: {tone_style}

USER QUERY: {user_query}

SEARCH RESULTS FROM SACRED TEXTS:
{search_results}

BASE ANALYSIS: {base_analysis}

RESPONSE INSTRUCTIONS:
{self.response_template.replace('{tone_style}', tone_style)}

Additional Tone Guidelines:
- If emotion is 'anger' or 'frustration': Validate their feelings while providing healing truth
- If emotion is 'despair' or 'yearning': Offer hope and authentic spiritual nourishment
- If emotion is 'confusion': Provide clear, step-by-step spiritual understanding
- If emotion is 'joy' or 'curiosity': Share in their enthusiasm while deepening insight
- Always maintain respect for their spiritual journey while exposing institutional deceptions

Focus on emotional resonance that matches their spiritual state while delivering transformative truth.
"""
        
        return {
            'prompt': emotional_prompt,
            'detected_emotion': emotion,
            'tone_style': optimal_tone,
            'spiritual_contexts': spiritual_contexts,
            'tone_description': tone_style
        }
    
    def create_emotional_response_metadata(self, user_query):
        """Create metadata about emotional response context"""
        
        emotion = self.detect_user_emotion(user_query)
        spiritual_contexts = self.analyze_spiritual_context(user_query)
        optimal_tone = self.determine_optimal_tone(emotion, spiritual_contexts)
        spiritual_intensity = self.detect_spiritual_intensity(user_query.lower())
        
        return {
            'emotional_analysis': {
                'primary_emotion': emotion,
                'spiritual_intensity': round(spiritual_intensity, 2),
                'contexts': spiritual_contexts,
                'recommended_tone': optimal_tone,
                'tone_description': self.tone_styles.get(optimal_tone, "scholarly"),
                'emotional_markers_found': self.get_detected_markers(user_query, emotion)
            },
            'response_strategy': {
                'approach': self.spiritual_tone_profiles.get(f"{emotion}_seeker", {
                    'spiritual_approach': 'truth_seeking',
                    'description': f'Addressing {emotion} with spiritual wisdom'
                }).get('spiritual_approach', 'truth_seeking'),
                'tone_adjustment': optimal_tone,
                'empathy_level': self.calculate_empathy_level(emotion, spiritual_intensity)
            }
        }
    
    def get_detected_markers(self, text, emotion):
        """Get the specific emotional markers detected in the text"""
        text_lower = text.lower()
        markers = []
        
        if emotion in self.emotion_detection_patterns:
            patterns_data = self.emotion_detection_patterns[emotion]
            
            # Find keyword markers
            for keyword in patterns_data['keywords']:
                if keyword in text_lower:
                    markers.append(f"keyword: {keyword}")
            
            # Find pattern markers  
            for pattern in patterns_data['patterns']:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    markers.append(f"pattern: {match}")
        
        return markers[:5]  # Return top 5 markers
    
    def calculate_empathy_level(self, emotion, spiritual_intensity):
        """Calculate appropriate empathy level for response"""
        
        # Base empathy levels by emotion
        base_empathy = {
            'joy': 0.7,
            'anger': 0.9, 
            'confusion': 0.8,
            'seeking': 0.6,
            'despair': 1.0,
            'curiosity': 0.5,
            'frustration': 0.8,
            'yearning': 0.9
        }
        
        base_level = base_empathy.get(emotion, 0.6)
        
        # Adjust based on spiritual intensity
        adjusted_level = base_level + (spiritual_intensity * 0.2)
        
        return min(adjusted_level, 1.0)  # Cap at 1.0
    
    def demonstrate_emotional_intelligence(self):
        """Demonstrate the emotional intelligence capabilities"""
        
        print("🎭 Divine Mirror AI - Emotional Tone Engine Demonstration")
        print("=" * 65)
        
        test_queries = [
            "I'm so angry at the church for lying to me about hell!",
            "I'm confused about what Jesus actually taught versus what churches say",
            "This is beautiful! I'm finding so much truth in these original texts", 
            "I feel lost and betrayed by everything I was taught growing up",
            "I'm desperately seeking authentic spiritual truth beyond religious manipulation",
            "What did Yeshua really teach about the Kingdom of Heaven?",
            "I'm curious about how Buddhism and Christianity compare on enlightenment"
        ]
        
        for query in test_queries:
            print(f"\n📝 User Query: \"{query}\"")
            
            # Analyze emotional context
            emotion = self.detect_user_emotion(query)
            contexts = self.analyze_spiritual_context(query)
            tone = self.determine_optimal_tone(emotion, contexts)
            intensity = self.detect_spiritual_intensity(query.lower())
            
            print(f"   🎭 Detected Emotion: {emotion}")
            print(f"   🔍 Spiritual Context: {', '.join(contexts) if contexts else 'general'}")
            print(f"   🎨 Optimal Tone: {tone} ({self.tone_styles[tone]})")
            print(f"   ⚡ Spiritual Intensity: {intensity:.2f}")
            
            # Show response strategy
            metadata = self.create_emotional_response_metadata(query)
            approach = metadata['response_strategy']['approach']
            empathy = metadata['response_strategy']['empathy_level']
            
            print(f"   💡 Response Strategy: {approach} (empathy: {empathy:.2f})")

def main():
    """Main demonstration function"""
    
    # Initialize emotional engine
    engine = EmotionalToneEngine()
    
    # Demonstrate capabilities
    engine.demonstrate_emotional_intelligence()
    
    print(f"\n✅ Phase 8 Emotional Tone Engine is fully operational!")
    print(f"🎭 Ready to provide emotionally intelligent spiritual guidance")
    print(f"🔧 Integrated with {len(engine.emotion_map)} emotion types and {len(engine.tone_styles)} response styles")

if __name__ == "__main__":
    main()