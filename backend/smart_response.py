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
            
            model_name = "deepseek-ai/deepseek-llm-r-7b-base"
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            print("Loading DeepSeek model...")
            deepseek_tokenizer = AutoTokenizer.from_pretrained(model_name)
            deepseek_model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
            print("DeepSeek ready.")
        except ImportError:
            print("DeepSeek dependencies not available. Install torch and transformers.")
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
    """Use DeepSeek model as fallback"""
    if not load_deepseek():
        return None
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = deepseek_tokenizer(prompt, return_tensors="pt").to(device)
        outputs = deepseek_model.generate(**inputs, max_new_tokens=max_tokens)
        return deepseek_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"DeepSeek Error: {e}")
        return None

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