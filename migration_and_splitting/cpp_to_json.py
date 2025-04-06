import openai
import json
import os
import ast  # Pentru parsing cod sursa


class CppToJsonAgent:
    def __init__(self, api_key, code_file_path):
        with open(code_file_path, 'r') as f:
            code = f.read()

        self.client = openai.OpenAI(api_key=api_key)
        self.system_prompt = f"""
You are a code analyzer.

Given the following code, split it into organized parts. Output in the following JSON format:

{{
    "libraries": {{ # only if there are any found (otherwise remove this part)
        "system": ["<system_includes>"],
        "custom": ["<custom_includes>"]
    }},
    "classes": {{ # only if there are any found (otherwise remove this part)
        "<class_name>": {{
            "description": "Brief description of what this class does",
            "code": "<complete_class_code>",
            "is_algorithm": "Complete with True if it is an implementation of an algorithm or False if not"
        }}
    }},
    "structs": {{ # only if there are any found (otherwise remove this part)
        "<struct_name>": {{
            "description": "Brief description of what this struct does",
            "code": "<complete_struct_code>",
            "is_algorithm": "Complete with True if it is an implementation of an algorithm or False if not"
        }}
    }},
    "functions": {{ # only if there are any found (otherwise remove this part)
        "<function_name>": {{
            "description": "Brief description of what this function does",
            "code": "<complete_function_code>",
            "is_algorithm": "Complete with True if it is an implementation of an algorithm or False if not"
        }}
    }},
    "main": {{ # only if there are any found (otherwise remove this part)
        "description": "Description of the main program flow",
        "code": "<main_function_code>",
        "is_algorithm": "Complete with True if it is an implementation of an algorithm or False if not"
    }}
}}

Important:
- Keep all methods within their class/struct definitions
- Keep descriptions short and focused on purpose/functionality
- Do not split member functions from their classes/structs
- Use the exact code formatting as in the source
- Do not insert .md tags (\\`\\`\\`json) in your output

Here is the code:
{code}
"""

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
        json_response = json.loads(response.choices[0].message.content)

        folder_name = "split_code_jsons"
        if not os.path.exists(folder_name): os.makedirs(folder_name)

        with open(os.path.join(folder_name, "code_analysis_1.json"), 'w') as f:
            json.dump(json_response, f, indent=4)

        return json_response


def get_json_descriptions(self):
    """Get the description fields from the generated JSON"""
    folder_name = "split_code_jsons"
    file_path = os.path.join(folder_name, "code_analysis_1.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        return json_data
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

