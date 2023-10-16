import json


def get_json_file_content(file_path: str) -> dict:
    """
    Function provides loading file content from json file to python object
    :param file_path: path to json file
    :return: dict with file content
    """
    with open(file_path, 'r') as file:
        result_json = json.load(file)

    return result_json
