import openai
import os
import ast  # Pentru parsing cod sursa
from tenacity import retry, wait_exponential, stop_after_attempt


class CodeMigrator:
    def __init__(self, api_key, prompt):
        self.client = openai.OpenAI(api_key=api_key)
        self.input_prompt = prompt

        self.prompt = f"""Act as a world-class Java developer. 
I want you to migrate the code that is parsed in the next block codes. 
Some of them have indications of implementation (an example of code I want you to use as refference and some of them are just code that I want you to migrate. 
Only write the code and add comments if you think that is necessary.
I want you to respect the implementation of the code that is parsed in the next part: \n

{self.input_prompt}"""


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