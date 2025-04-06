import openai
import os
from tenacity import retry, wait_exponential, stop_after_attempt


class RagSelectorAgent:
    def __init__(self, api_key, description, path='RAG/thealgorithms'):
        self.client = openai.OpenAI(api_key=api_key)
        self.description = description

        if path == 'RAG/thealgorithms':
            search_path = self.get_subdirectories(path)
        else:
            search_path = self.get_file_names(path)

        # System prompt_old configurable
        self.system_prompt = f"""
Act as a world-class Java developer. Your task:
1. Analyze this NLP description: {self.description}.
2. Choose the type of algorithm that best matches the description from the provided list of algorithms: {search_path}.
3. You must only respond with the selected category that matches the description. If none of them are matching, return "None".
4. Do not add any explanations or additional information.
"""

    @retry(wait=wait_exponential(multiplier=1, min=2, max=60),
           stop=stop_after_attempt(3))
    def _api_call(self):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.system_prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )
        print(f"Tokens used: {response.usage}")
        return response.choices[0].message.content

    def get_subdirectories(self, directory):
        return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory))]

    def get_file_names(self, directory):
        return [os.path.splitext(name)[0] for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]


