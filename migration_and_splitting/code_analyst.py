import openai
import os
import ast  # Pentru parsing cod sursa
from tenacity import retry, wait_exponential, stop_after_attempt


class CodeAnalystAgent:
    def __init__(self, api_key, file_path, input_prompt):
        self.client = openai.OpenAI(api_key=api_key)
        self.path = file_path
        self.prompt = input_prompt


    @retry(wait=wait_exponential(multiplier=1, min=2, max=60),
           stop=stop_after_attempt(3))
    def _api_call(self):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )
        print(f"Tokens used: {response.usage}")
        return response.choices[0].message.content
