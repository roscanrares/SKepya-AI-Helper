import openai
from tenacity import retry, wait_exponential, stop_after_attempt
import json

def json_to_string(json_data):
    result = ""
    cnt = 0  # Declare cnt in the enclosing scope

    def iterate_elements(obj, indent=0):
        nonlocal result, cnt  # Use nonlocal to modify cnt
        if isinstance(obj, dict):
            for index, (key, value) in enumerate(obj.items()):
                if key == "code" and "is_algorithm" in obj:
                    result += f"{cnt + 1}. Part number {cnt + 1} of the code:\n {value} "
                    cnt += 1
                    if obj["is_algorithm"] != "False":
                        print("Algorithm detected:\n", obj["is_algorithm"])
                        result += f"I want you to use as inspiration and respect the implementation of this code in migration \n{obj['is_algorithm']}\n \n \n"
                elif key == "libraries":
                    result += f"These are the libraries used in the original code:\n{key}:\n"
                    iterate_elements(value, indent + 2)
                elif isinstance(value, (dict, list)):
                    iterate_elements(value, indent)
        elif isinstance(obj, list):
            for item in obj:
                result += f"{' ' * indent}- {item}\n"
        else:
            result += f"{' ' * indent}{obj}\n"

    iterate_elements(json_data)
    return result

# Read the JSON file
def run_json_to_string():
    with open('split_code_jsons/code_analysis_2.json', 'r') as file:
        json_data = json.load(file)

    prompt = json_to_string(json_data)
    return prompt


