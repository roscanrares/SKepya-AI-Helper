import json


def create_description_dict(json_path):
    description_dict = {}
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    def extract_descriptions(obj, index=0):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "description":
                    description = value
                    is_algorithm = obj.get("is_algorithm", "False") == "True"
                    description_dict[index] = {"description": description, "is_algorithm": is_algorithm}
                    index += 1
                else:
                    index = extract_descriptions(value, index)
        elif isinstance(obj, list):
            for item in obj:
                index = extract_descriptions(item, index)
        return index

    extract_descriptions(json_data)
    return description_dict

def update_is_algorithm(json_data, target_description, new_value):
    """
    Update the "is_algorithm" field in the JSON data based on the target description.
    :param json_data:
    :param target_description:
    :param new_value:
    :return:
    """

    def search_and_update(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "description" and value == target_description:
                    obj["is_algorithm"] = new_value
                elif isinstance(value, dict) or isinstance(value, list):
                    search_and_update(value)
        elif isinstance(obj, list):
            for item in obj:
                search_and_update(item)

    search_and_update(json_data)
