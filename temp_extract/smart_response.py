
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import openai

# --- Configure your OpenAI Key ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- DeepSeek Setup ---
model_name = "deepseek-ai/deepseek-llm-r-7b-base"
device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading DeepSeek model...")
deepseek_tokenizer = AutoTokenizer.from_pretrained(model_name)
deepseek_model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
print("DeepSeek ready.")

def use_openai(prompt, model="gpt-4", max_tokens=200):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except openai.error.RateLimitError:
        return None
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None

def use_deepseek(prompt, max_tokens=200):
    inputs = deepseek_tokenizer(prompt, return_tensors="pt").to(device)
    outputs = deepseek_model.generate(**inputs, max_new_tokens=max_tokens)
    return deepseek_tokenizer.decode(outputs[0], skip_special_tokens=True)

def smart_generate(prompt, user_tokens_today=0, max_daily_tokens=10000, model="gpt-4"):
    if user_tokens_today >= max_daily_tokens:
        print("Token limit reached, using DeepSeek.")
        return use_deepseek(prompt)

    result = use_openai(prompt, model=model)
    if result is None:
        print("OpenAI failed or throttled. Falling back to DeepSeek.")
        return use_deepseek(prompt)
    return result
