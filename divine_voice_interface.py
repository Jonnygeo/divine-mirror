#!/usr/bin/env python3
"""
Divine Mirror AI - Voice Interface Backend
Handles voice-to-text processing and text-to-speech responses
"""

import os
import json
import tempfile
from pathlib import Path
import subprocess

class VoiceInterface:
    """Voice interface for Divine Mirror AI"""
    
    def __init__(self, enhanced_index_file="divine_enhanced_index.json"):
        self.load_enhanced_index(enhanced_index_file)
        self.supported_languages = {
            'en': 'English',
            'he': 'Hebrew', 
            'gr': 'Greek',
            'ar': 'Arabic',
            'sa': 'Sanskrit',
            'la': 'Latin'
        }
    
    def load_enhanced_index(self, filename):
        """Load the enhanced search index"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data['documents']
            self.metadata_index = data['metadata_index'] 
            self.word_index = {word: set(doc_ids) for word, doc_ids in data['word_index'].items()}
            self.tag_statistics = data.get('tag_statistics', {})
            
            print(f"✅ Voice interface loaded: {len(self.documents)} documents")
            
        except FileNotFoundError:
            print("❌ Enhanced index not found. Run divine_intelligent_tagger.py first.")
            self.documents = []
    
    def detect_language(self, text):
        """Simple language detection based on character patterns"""
        # Hebrew characters
        if any('\u0590' <= char <= '\u05FF' for char in text):
            return 'he'
        
        # Greek characters
        if any('\u0370' <= char <= '\u03FF' for char in text):
            return 'gr'
        
        # Arabic characters
        if any('\u0600' <= char <= '\u06FF' for char in text):
            return 'ar'
        
        # Sanskrit/Devanagari characters
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'sa'
        
        # Default to English
        return 'en'
    
    def search_voice_query(self, query, max_results=3):
        """Process voice query and return relevant results"""
        if not self.documents or not query.strip():
            return []
        
        # Simple keyword extraction
        words = query.lower().split()
        search_words = [word for word in words if len(word) > 2]
        
        if not search_words:
            return []
        
        # Score documents
        doc_scores = {}
        for doc in self.documents:
            score = 0
            text_lower = doc['text'].lower()
            
            # Score by word matches
            for word in search_words:
                if word in text_lower:
                    score += text_lower.count(word)
            
            if score > 0:
                doc_scores[doc['id']] = {
                    'score': score,
                    'document': doc['text'][:300] + "...",
                    'metadata': doc['metadata']
                }
        
        # Sort by relevance and return top results
        sorted_results = sorted(doc_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        results = []
        for doc_id, data in sorted_results[:max_results]:
            results.append({
                'tradition': data['metadata'].get('tradition', 'Unknown'),
                'title': data['metadata'].get('title', 'Unknown'),
                'text': data['document'],
                'score': data['score']
            })
        
        return results
    
    def format_voice_response(self, results, query):
        """Format search results for voice response"""
        if not results:
            return f"I found no results for your query about {query}. Try asking about concepts like love, wisdom, or divine nature."
        
        response = f"I found {len(results)} relevant passages for your query about {query}. "
        
        for i, result in enumerate(results, 1):
            tradition = result['tradition']
            title = result['title']
            
            # Clean text for speech
            text = result['text'].replace('📘', '').replace('📜', '').replace('✅', '')
            text = text.replace('\n', ' ').strip()
            
            # Limit text length for voice
            if len(text) > 200:
                text = text[:200] + "..."
            
            response += f"Result {i}: From the {tradition} tradition, {title} says: {text}. "
        
        return response
    
    def process_voice_command(self, transcript):
        """Process voice command and return formatted response"""
        print(f"🎤 Processing voice query: '{transcript}'")
        
        # Detect language
        detected_lang = self.detect_language(transcript)
        lang_name = self.supported_languages.get(detected_lang, 'Unknown')
        
        print(f"🌍 Detected language: {lang_name}")
        
        # Search for results
        results = self.search_voice_query(transcript)
        
        # Format response
        response = self.format_voice_response(results, transcript)
        
        return {
            'query': transcript,
            'detected_language': detected_lang,
            'language_name': lang_name,
            'results_count': len(results),
            'response_text': response,
            'detailed_results': results
        }
    
    def create_audio_response(self, text, output_file="voice_response.wav"):
        """Create audio response using system TTS (cross-platform)"""
        try:
            # Try different TTS systems based on platform
            
            # Linux: espeak
            if subprocess.run(['which', 'espeak'], capture_output=True).returncode == 0:
                subprocess.run([
                    'espeak', 
                    '-s', '150',  # Speed
                    '-v', 'en',   # Voice
                    '-w', output_file,  # Write to file
                    text
                ], check=True)
                return True
            
            # macOS: say
            elif subprocess.run(['which', 'say'], capture_output=True).returncode == 0:
                subprocess.run([
                    'say', 
                    '-v', 'Alex',
                    '-o', output_file,
                    text
                ], check=True)
                return True
            
            # Windows: PowerShell SAPI
            elif os.name == 'nt':
                ps_command = f'''
                Add-Type –AssemblyName System.Speech;
                $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
                $synth.SetOutputToWaveFile("{output_file}");
                $synth.Speak("{text}");
                $synth.Dispose();
                '''
                subprocess.run(['powershell', '-Command', ps_command], check=True)
                return True
            
            else:
                print("⚠️ No TTS system available")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ TTS error: {e}")
            return False
        except Exception as e:
            print(f"❌ Audio creation error: {e}")
            return False

def main():
    """Test the voice interface"""
    interface = VoiceInterface()
    
    if not interface.documents:
        print("No documents loaded. Run divine_intelligent_tagger.py first.")
        return
    
    print("🎤 Divine Mirror AI - Voice Interface Test")
    print("=" * 45)
    
    # Test queries
    test_queries = [
        "What did Jesus teach about love?",
        "Buddhist teachings on suffering",
        "Tao and natural harmony",
        "Divine nature in Hinduism"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        response = interface.process_voice_command(query)
        
        print(f"📊 Results: {response['results_count']} found")
        print(f"🗣️ Response: {response['response_text'][:200]}...")
        
        # Create audio file
        audio_file = f"test_response_{query.replace(' ', '_')[:20]}.wav"
        if interface.create_audio_response(response['response_text'], audio_file):
            print(f"🔊 Audio saved: {audio_file}")
        
        print("-" * 40)

if __name__ == "__main__":
    main()