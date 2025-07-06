
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load DeepSeek-R1 model
print("Loading DeepSeek-R1 model... This may take a moment.")

model_name = "deepseek-ai/deepseek-llm-r-7b-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Try GPU first, fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto" if device == "cuda" else None)
model = model.to(device)

print("DeepSeek-R1 is ready.")

def generate_response(prompt: str, max_tokens: int = 300) -> str:
    """
    Generate a response using the DeepSeek-R1 model.

    Args:
        prompt (str): The input prompt to guide the response.
        max_tokens (int): Maximum number of tokens to generate.

    Returns:
        str: The generated response from the model.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
