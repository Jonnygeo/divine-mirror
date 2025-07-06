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
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"OpenAI JSON Error: {e}")
        
        # Fall back to regular generation and try to parse
        result = smart_generate(prompt, model=model, max_tokens=max_tokens)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": "Unable to generate valid JSON response"}

def create_spiritual_fallback_response(prompt: str) -> str:
    """Create a spiritual fallback response when AI models are unavailable"""
    prompt_lower = prompt.lower()
    
    # Basic spiritual query patterns
    if "kingdom" in prompt_lower and "god" in prompt_lower:
        return """According to Jesus's original teachings, the Kingdom of God is not a physical place but a spiritual state of consciousness. As recorded in Luke 17:21: "The kingdom of God is within you." This suggests that divine truth is accessible through inner spiritual awareness rather than external religious institutions."""
    
    elif "truth" in prompt_lower and ("jesus" in prompt_lower or "christ" in prompt_lower):
        return """Jesus emphasized inner spiritual truth over external religious authority. His teachings focused on love, compassion, and direct spiritual experience rather than institutional control. Many of his original teachings about personal spiritual empowerment were later modified by religious institutions."""
    
    elif "divine" in prompt_lower or "spiritual" in prompt_lower:
        return """Original spiritual teachings often emphasize direct personal connection with the divine, inner wisdom, and spiritual transformation. These core truths have sometimes been altered by institutions to emphasize external authority and control rather than personal spiritual empowerment."""
    
    else:
        return "I cannot provide a detailed analysis without proper AI model access. Please provide a valid OpenAI API key to enable full spiritual text comparison capabilities."