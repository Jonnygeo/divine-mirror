/**
 * Divine Mirror AI - Voice Interface Frontend
 * Handles speech recognition and text-to-speech for web interface
 */

class DivineVoiceInterface {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.currentLanguage = 'en-US';
        this.setupSpeechRecognition();
        this.setupEventListeners();
    }

    setupSpeechRecognition() {
        // Check for speech recognition support
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.maxAlternatives = 1;
            this.recognition.lang = this.currentLanguage;

            this.recognition.onstart = () => {
                this.onSpeechStart();
            };

            this.recognition.onresult = (event) => {
                this.onSpeechResult(event);
            };

            this.recognition.onerror = (event) => {
                this.onSpeechError(event);
            };

            this.recognition.onend = () => {
                this.onSpeechEnd();
            };

            console.log('✅ Speech recognition initialized');
        } else {
            console.warn('⚠️ Speech recognition not supported in this browser');
            this.showNotification('Speech recognition not supported in this browser', 'warning');
        }
    }

    setupEventListeners() {
        // Voice button
        const voiceBtn = document.getElementById('voiceButton');
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => this.toggleListening());
        }

        // Language selector
        const langSelect = document.getElementById('languageSelect');
        if (langSelect) {
            langSelect.addEventListener('change', (e) => {
                this.changeLanguage(e.target.value);
            });
        }

        // Stop speaking button
        const stopBtn = document.getElementById('stopSpeakingButton');
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopSpeaking());
        }
    }

    toggleListening() {
        if (!this.recognition) {
            this.showNotification('Speech recognition not available', 'error');
            return;
        }

        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        if (!this.recognition || this.isListening) return;

        try {
            this.recognition.start();
            this.updateVoiceButton('listening');
            this.showNotification('Listening... Speak your query', 'info');
        } catch (error) {
            console.error('Speech recognition start error:', error);
            this.showNotification('Could not start speech recognition', 'error');
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    onSpeechStart() {
        this.isListening = true;
        console.log('🎤 Speech recognition started');
    }

    onSpeechResult(event) {
        const transcript = event.results[0][0].transcript;
        const confidence = event.results[0][0].confidence;
        
        console.log('📝 Transcript:', transcript, 'Confidence:', confidence);
        
        // Update search input
        const searchInput = document.getElementById('searchInput') || document.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.value = transcript;
        }

        // Show transcript
        this.showTranscript(transcript, confidence);

        // Process the query
        this.processVoiceQuery(transcript);
    }

    onSpeechError(event) {
        console.error('🚨 Speech recognition error:', event.error);
        
        let errorMessage = 'Speech recognition error';
        switch (event.error) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone access. Please check permissions.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone access denied. Please allow microphone access.';
                break;
            case 'network':
                errorMessage = 'Network error. Please check your connection.';
                break;
            default:
                errorMessage = `Speech recognition error: ${event.error}`;
        }
        
        this.showNotification(errorMessage, 'error');
        this.updateVoiceButton('idle');
    }

    onSpeechEnd() {
        this.isListening = false;
        this.updateVoiceButton('idle');
        console.log('🏁 Speech recognition ended');
    }

    async processVoiceQuery(transcript) {
        try {
            this.showLoading(true);
            
            // Send to backend for processing
            const response = await fetch('/api/voice-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: transcript,
                    language: this.currentLanguage
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Display results
            this.displayVoiceResults(data);
            
            // Speak response
            if (data.response_text) {
                this.speakResponse(data.response_text);
            }

        } catch (error) {
            console.error('Voice query error:', error);
            this.showNotification('Error processing voice query', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    speakResponse(text, language = 'en-US') {
        if ('speechSynthesis' in window) {
            // Stop any current speech
            speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = language;
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 0.8;

            // Get available voices
            const voices = speechSynthesis.getVoices();
            if (voices.length > 0) {
                // Prefer female voices for spiritual content
                const preferredVoice = voices.find(voice => 
                    voice.lang.startsWith(language.split('-')[0]) && 
                    (voice.name.includes('Female') || voice.name.includes('Samantha') || voice.name.includes('Karen'))
                ) || voices.find(voice => voice.lang.startsWith(language.split('-')[0]));
                
                if (preferredVoice) {
                    utterance.voice = preferredVoice;
                }
            }

            utterance.onstart = () => {
                this.updateSpeakingStatus(true);
                console.log('🗣️ Started speaking response');
            };

            utterance.onend = () => {
                this.updateSpeakingStatus(false);
                console.log('🏁 Finished speaking response');
            };

            utterance.onerror = (event) => {
                console.error('Speech synthesis error:', event);
                this.updateSpeakingStatus(false);
            };

            speechSynthesis.speak(utterance);
        } else {
            console.warn('⚠️ Speech synthesis not supported');
            this.showNotification('Text-to-speech not supported in this browser', 'warning');
        }
    }

    stopSpeaking() {
        if ('speechSynthesis' in window) {
            speechSynthesis.cancel();
            this.updateSpeakingStatus(false);
            console.log('🛑 Stopped speaking');
        }
    }

    changeLanguage(languageCode) {
        this.currentLanguage = languageCode;
        if (this.recognition) {
            this.recognition.lang = languageCode;
        }
        console.log('🌍 Language changed to:', languageCode);
        this.showNotification(`Language changed to ${languageCode}`, 'info');
    }

    updateVoiceButton(state) {
        const voiceBtn = document.getElementById('voiceButton');
        if (!voiceBtn) return;

        const icon = voiceBtn.querySelector('.voice-icon');
        const text = voiceBtn.querySelector('.voice-text');

        switch (state) {
            case 'listening':
                voiceBtn.classList.add('listening');
                voiceBtn.disabled = false;
                if (icon) icon.textContent = '🛑';
                if (text) text.textContent = 'Stop Listening';
                break;
            case 'processing':
                voiceBtn.classList.remove('listening');
                voiceBtn.disabled = true;
                if (icon) icon.textContent = '⏳';
                if (text) text.textContent = 'Processing...';
                break;
            case 'idle':
            default:
                voiceBtn.classList.remove('listening');
                voiceBtn.disabled = false;
                if (icon) icon.textContent = '🎤';
                if (text) text.textContent = 'Voice Search';
                break;
        }
    }

    updateSpeakingStatus(isSpeaking) {
        const statusElement = document.getElementById('speakingStatus');
        const stopBtn = document.getElementById('stopSpeakingButton');

        if (statusElement) {
            statusElement.style.display = isSpeaking ? 'block' : 'none';
        }

        if (stopBtn) {
            stopBtn.style.display = isSpeaking ? 'inline-block' : 'none';
        }
    }

    showTranscript(transcript, confidence) {
        const transcriptElement = document.getElementById('voiceTranscript');
        if (transcriptElement) {
            transcriptElement.innerHTML = `
                <div class="transcript-result">
                    <strong>You said:</strong> "${transcript}"
                    <span class="confidence">(${Math.round(confidence * 100)}% confidence)</span>
                </div>
            `;
            transcriptElement.style.display = 'block';
        }
    }

    displayVoiceResults(data) {
        const resultsContainer = document.getElementById('voiceResults');
        if (!resultsContainer) return;

        let html = `
            <div class="voice-response">
                <h3>🔍 Voice Search Results</h3>
                <p><strong>Query:</strong> "${data.query}"</p>
                <p><strong>Language:</strong> ${data.language_name}</p>
                <p><strong>Results Found:</strong> ${data.results_count}</p>
            </div>
        `;

        if (data.detailed_results && data.detailed_results.length > 0) {
            html += '<div class="voice-results-list">';
            
            data.detailed_results.forEach((result, index) => {
                html += `
                    <div class="voice-result-item">
                        <h4>${index + 1}. ${result.tradition} - ${result.title}</h4>
                        <p class="result-text">${result.text}</p>
                        <span class="result-score">Relevance: ${result.score}</span>
                    </div>
                `;
            });
            
            html += '</div>';
        }

        resultsContainer.innerHTML = html;
        resultsContainer.style.display = 'block';
    }

    showLoading(show) {
        const loadingElement = document.getElementById('voiceLoading');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `voice-notification ${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);

        console.log(`📢 ${type.toUpperCase()}: ${message}`);
    }
}

// Initialize voice interface when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.divineVoice = new DivineVoiceInterface();
    console.log('🎤 Divine Mirror Voice Interface initialized');
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DivineVoiceInterface;
}