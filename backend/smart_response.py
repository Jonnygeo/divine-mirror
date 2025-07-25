import os
import json
from typing import Optional
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DeepSeek fallback (lazy loading to avoid startup issues)
deepseek_model = None
deepseek_tokenizer = None

def load_deepseek():
    """Lazy load DeepSeek model when needed"""
    global deepseek_model, deepseek_tokenizer
    if deepseek_model is None:
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # Use a smaller, more efficient model for this environment
            model_name = "microsoft/DialoGPT-medium"  # Fallback to a smaller model
            device = "cpu"  # Force CPU to avoid CUDA issues
            
            print("Loading fallback model (DialoGPT-medium)...")
            deepseek_tokenizer = AutoTokenizer.from_pretrained(model_name)
            deepseek_model = AutoModelForCausalLM.from_pretrained(model_name)
            print("Fallback model ready.")
        except ImportError:
            print("Transformers dependencies not available. Using built-in fallback.")
            return False
        except Exception as e:
            print(f"Error loading fallback model: {e}")
            return False
    return True

def use_openai(prompt: str, model: str = "gpt-4o", max_tokens: int = 500) -> Optional[str]:
    """Use OpenAI API with error handling"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None

def use_deepseek(prompt: str, max_tokens: int = 500) -> Optional[str]:
    """Use simple text-based fallback when transformers not available"""
    if not load_deepseek():
        # Simple rule-based fallback for spiritual/religious queries
        if any(word in prompt.lower() for word in ["kingdom", "god", "jesus", "spiritual", "divine", "truth"]):
            return create_spiritual_fallback_response(prompt)
        else:
            return "I cannot process this request without proper AI model access. Please provide a valid OpenAI API key."
    
    try:
        device = "cpu"  # Force CPU usage
        inputs = deepseek_tokenizer(prompt, return_tensors="pt")
        outputs = deepseek_model.generate(**inputs, max_new_tokens=max_tokens, pad_token_id=deepseek_tokenizer.eos_token_id)
        return deepseek_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Fallback Model Error: {e}")
        return create_spiritual_fallback_response(prompt)

def smart_generate(prompt: str, model: str = "gpt-4o", max_tokens: int = 500) -> str:
    """
    Smart model switching: tries OpenAI first, falls back to DeepSeek if needed
    """
    # Try OpenAI first
    result = use_openai(prompt, model=model, max_tokens=max_tokens)
    
    if result is None:
        print("OpenAI failed or throttled. Falling back to DeepSeek.")
        result = use_deepseek(prompt, max_tokens=max_tokens)
        
        if result is None:
            return "I apologize, but I'm currently unable to generate a response. Please try again later."
    
    return result

def smart_generate_json(prompt: str, model: str = "gpt-4o", max_tokens: int = 500) -> dict:
    """
    Smart model switching for JSON responses
    """
    # Try OpenAI first with JSON mode
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content.strip())
        # Check if result has meaningful content
        if not any(result.get(key) for key in ['original_teachings', 'modern_interpretations', 'comparison']):
            print("OpenAI returned empty content, triggering fallback")
            return {"needs_fallback": True}
        return result
    except Exception as e:
        print(f"OpenAI JSON Error: {e}")
        
        # Fall back to regular generation and try to parse
        result = smart_generate(prompt, model=model, max_tokens=max_tokens)
        try:
            parsed = json.loads(result)
            if not any(parsed.get(key) for key in ['original_teachings', 'modern_interpretations', 'comparison']):
                print("Fallback model returned empty content")
                return {"needs_fallback": True}
            return parsed
        except json.JSONDecodeError:
            print("Unable to parse JSON, triggering fallback")
            return {"needs_fallback": True}

def create_spiritual_fallback_response(prompt: str) -> str:
    """Create a spiritual fallback response based on Yeshua's authentic teachings"""
    prompt_lower = prompt.lower()
    
    # Kingdom of God queries
    if "kingdom" in prompt_lower and ("god" in prompt_lower or "heaven" in prompt_lower):
        return """According to Yeshua's original teachings, the Kingdom of God is within you (Luke 17:21), not a physical place or external institution. As recorded in the Gospel of Thomas (Saying 3): "The Kingdom is inside you and outside you. If you know yourselves, then you will be known." This inner spiritual state is accessible through direct divine awareness, bypassing religious intermediaries. The Church externalized this teaching to maintain control through sacraments and hierarchy, contradicting Yeshua's message of personal spiritual empowerment."""
    
    # Truth vs. control themes
    elif ("truth" in prompt_lower or "control" in prompt_lower) and ("jesus" in prompt_lower or "yeshua" in prompt_lower or "church" in prompt_lower):
        return """Yeshua taught "You will know the truth, and the truth will set you free" (John 8:32), emphasizing liberation through direct knowledge of God. He rejected hierarchical titles, saying "You have one Teacher, and you are all brothers" (Matthew 23:8-10). However, post-Constantine Christianity centralized authority through papal supremacy and sacramental control. The Council of Nicaea (325 CE) prioritized institutional control over Yeshua's original message of spiritual freedom. Non-canonical texts like the Gospel of Thomas preserve his authentic teachings about inner truth over external authority."""
    
    # Love vs. ritual themes  
    elif ("love" in prompt_lower or "ritual" in prompt_lower or "mercy" in prompt_lower) and ("jesus" in prompt_lower or "yeshua" in prompt_lower):
        return """Yeshua taught "I desire mercy, not sacrifice" (Matthew 9:13), prioritizing compassion over ritual performance. His message was universal love: "Love your neighbor as yourself" (Mark 12:31). The Church later reintroduced ritualism through sacraments, making salvation priest-dependent rather than based on mercy and love. The Council of Trent (1545-1563) codified this control system, contradicting Yeshua's direct mercy-based approach seen in stories like the woman at the well and forgiving the adulterous woman."""
    
    # Religious hypocrisy themes
    elif ("hypocrisy" in prompt_lower or "pharisees" in prompt_lower or "religious" in prompt_lower) and ("elite" in prompt_lower or "leaders" in prompt_lower):
        return """Yeshua condemned religious hypocrisy: "Woe to you, teachers of the law and Pharisees, you hypocrites!" (Matthew 23:13-39). He called them "whitewashed tombs, beautiful on the outside but full of dead bones" (Matthew 23:27). When he expelled money-changers from the temple (John 2:13-16), he rejected profiting from faith. Ironically, the Catholic Church replicated this hypocrisy with indulgences, tithing monopolies, and sacramental control - becoming the very religious elite Yeshua opposed."""
    
    # Biblical manipulation themes
    elif ("bible" in prompt_lower or "scripture" in prompt_lower) and ("changed" in prompt_lower or "added" in prompt_lower or "manipulation" in prompt_lower):
        return """Many biblical terms were mistranslated to support institutional control: 'Hell' (Gehenna) was a literal garbage dump near Jerusalem, not a cosmic torture chamber. 'Repent' (metanoia) means change of mind/heart, not groveling. 'Sin' (hamartia) means missing the mark, not eternal damnation. The Vulgate translations amplified fear-based terms. Textual additions like the Comma Johanneum (1 John 5:7-8) were inserted to enforce Trinitarian doctrine. Non-canonical texts like the Gospel of Thomas were excluded because they preserved Yeshua's original empowering message."""
    
    # General spiritual truth  
    elif "divine" in prompt_lower or "spiritual" in prompt_lower or "god" in prompt_lower:
        return """Original spiritual teachings emphasize direct personal connection with the divine, inner wisdom, and spiritual transformation. As Yeshua taught, "True worshipers will worship the Father in spirit and truth" (John 4:23-24). These core truths have been systematically altered by institutions to emphasize external authority and control rather than personal spiritual empowerment. The excluded Gospel of Mary teaches that truth comes from within, not through laws or leaders - precisely why such texts were suppressed."""
    
    else:
        return "For detailed spiritual text comparison and analysis of Yeshua's authentic teachings versus institutional manipulations, please provide a valid OpenAI API key to access the full Divine Mirror AI capabilities with comprehensive biblical analysis."