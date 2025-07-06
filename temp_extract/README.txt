
README: Replit AI Model Switcher for GPT + DeepSeek
===================================================

INSTRUCTIONS FOR AGENT:
------------------------

1. Place 'smart_response.py' in your app's main folder.
2. In your main code where you generate AI output, replace this:

   from openai import ChatCompletion
   # ... your old OpenAI logic

   WITH THIS:

   from smart_response import smart_generate

   result = smart_generate(prompt, user_tokens_today=stored_token_count)

   # You can also use:
   # result = smart_generate(prompt, user_tokens_today=0, max_daily_tokens=10000, model="gpt-4")

3. Ensure the following are installed in `requirements.txt`:

   torch
   transformers
   openai

4. Set your OPENAI_API_KEY in the Replit secrets tab.

5. This script will:
   - Use GPT-4 when under quota
   - Fall back to DeepSeek when over quota or throttled
   - Ensure continued generation without crashing your app

This module can be copied and reused across all your Replit projects.

