import cpp_to_json
import migration_prompt_generator
import rag_selector
import description_fetch
import code_generator
import os
import json
import code_generator
from code_generator import CodeMigrator
from code_analyst import CodeAnalystAgent
from migration_prompt_generator import run_json_to_string
from dotenv import load_dotenv
import sys


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def migration(file_path):
    cpp_code_file_path = file_path
    agent_cpp_to_json = cpp_to_json.CppToJsonAgent(
        api_key=api_key,
        code_file_path=cpp_code_file_path
    )
    splitted = agent_cpp_to_json._api_call()
    with open('split_code_jsons/code_analysis_1.json', 'r') as f:
        code_analysis = json.load(f)

    descriptions = description_fetch.create_description_dict('split_code_jsons/code_analysis_1.json')
    path = 'RAG/thealgorithms'
    for key, description in descriptions.items():
        if description['is_algorithm']:
            agent_rag = rag_selector.RagSelectorAgent(
                api_key=api_key,
                description=description,
                path=path
            )
            rag_selection = agent_rag._api_call()
            if rag_selection is not None:
                new_search_path = os.path.join(path + '/' + rag_selection)
                agent_rag = rag_selector.RagSelectorAgent(
                    api_key=api_key,
                    description=description,
                    path=new_search_path
                )
                rag_selection_2 = agent_rag._api_call()

                print(f"\nRAG selection for {key}: {rag_selection_2}\n")

                if rag_selection_2 is not None and not True:
                    java_snippet_path = new_search_path + '/' + rag_selection_2 + '.java'
                    with open(java_snippet_path, 'r') as f:
                        java_snippet = f.read()
                    description_fetch.update_is_algorithm(code_analysis, description['description'], java_snippet)
                else:
                    description_fetch.update_is_algorithm(code_analysis, description['description'], "")

    # After changing the descriptions['is_algorithm[, make a json dump to a second json file
    with open('split_code_jsons/code_analysis_2.json', 'w') as f:
        json.dump(code_analysis, f, indent=4)

    # Now we have the second json file with the descriptions and the code snippets
    given_prompt = run_json_to_string()
    agent_prompt = CodeMigrator(
        api_key=api_key,
        prompt=given_prompt
    )

    generated_prompt = agent_prompt._api_call()

    with open("migrated/migrated_code.md", "w") as f:
        f.write(generated_prompt)


def code_generation(prompt):
    file_name, file_extension = os.path.splitext(file_path)
    agent_code_gen = code_generator.CodeGeneratorAgent(
        api_key=api_key,
        prompt=prompt
    )
    generated_code = agent_code_gen._api_call()
    with open("generated_code.txt", "w") as f:
        f.write(generated_code)

    agent_cpp_to_json = cpp_to_json.CppToJsonAgent(
        api_key=api_key,
        code_file_path=file_path
    )


def readme_generator(file_path):
    agent_cpp_to_json = cpp_to_json.CppToJsonAgent(
        api_key=api_key,
        code_file_path=file_path
    )
    splitted = agent_cpp_to_json._api_call()
    prompt = f"You are a conde analyst. You have to generate a readme file for the code provided. The readme file should contain the following sections:\n\n{splitted}\n\n"
    agent_readme_generator = CodeAnalystAgent(
        api_key=api_key,
        file_path=file_path,
        input_prompt=prompt
    )
    generated_readme = agent_readme_generator._api_call()


    with open("code_analysis/generated_readme.md", "w") as f:
        f.write(generated_readme)


def comments_generator(file_path):
    file_name, file_extension = os.path.splitext(file_path)

    agent_cpp_to_json = cpp_to_json.CppToJsonAgent(
        api_key=api_key,
        code_file_path=file_path
    )
    splitted = agent_cpp_to_json._api_call()
    prompt = f"You are a code analyst. You have to comment the following code. The code should have comprehensive comments for each part of the code that exaplins that part and more in depths in each line of code:\n\n{splitted}\n\n"
    agent_readme_generator = CodeAnalystAgent(
        api_key=api_key,
        file_path=file_path,
        input_prompt=prompt
    )
    generated_readme = agent_readme_generator._api_call()
    with open(f"code_analysis/commented_code{file_extension}", "w") as f:
        f.write(generated_readme)

def refactor_variables(file_path, case_type="snake_case"):
    file_name, file_extension = os.path.splitext(file_path)

    with open(file_path, 'r') as f:
        code = f.read()
    prompt = f"You are a code analyst. Assign proper variables names and use the {case_type} for the following code.\n\n{code}\n\n"

    agent_transform_variables = CodeAnalystAgent(
        api_key=api_key,
        file_path=file_path,
        input_prompt=prompt
    )
    transformed_code = agent_transform_variables._api_call()

    with open(f"code_analysis/generated_variables_code{file_extension}", "w") as f:
        f.write(transformed_code)

def test_creation(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    agent_cpp_to_json = cpp_to_json.CppToJsonAgent(
        api_key=api_key,
        code_file_path=file_path
    )
    splitted = agent_cpp_to_json._api_call()
    prompt = f"You are a proffesional quallity assurance engineer. You have to generate a test file for the code provided. The test file should contain the following sections:\n\n{splitted}\n\n"
    agent_test_creation = CodeAnalystAgent(
        api_key=api_key,
        file_path=file_path,
        input_prompt=prompt
    )
    generated_code = agent_test_creation._api_call()

    with open(f"code_analysis/generated_test_creation{file_extension}", "w") as f:
        f.write(generated_code)


if __name__ == "__main__":
    comments_generator('demo_cpp_files/t1.cpp')
    # Example usage
    if len(sys.argv) > -1:
        function_name = 'migration'
        # file_path = sys.argv[1]

        if function_name == "migration":
            file_path = 'demo_cpp_files/t1.cpp'
            migration(file_path)

        elif function_name == "code_generation":
            prompt = sys.argv[1]
            code_generation(prompt)
        else:
            print("Please provide the function name and the file path or prompt.")
