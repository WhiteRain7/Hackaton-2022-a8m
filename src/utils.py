import requests
import json
import pathlib

DIRECTORY_FILES = pathlib.Path(__file__).parent.absolute() / 'files'


def get_json_from_url(url: str) -> dict:
    try:
        parsed_data = requests.get(url).json()
        return parsed_data
    except Exception as e:
        print(e)
        return {}


def write_list_to_file(file_name: str, data: list):
    json_object = json.dumps(data, indent=1)
    with open(DIRECTORY_FILES / file_name, "w") as outfile:
        outfile.write(json_object)


def read_file_to_list(file_name: str) -> list:
    with open(DIRECTORY_FILES / file_name, "r") as openfile:
        data = json.load(openfile)
    return data


def to_float(x: any) -> float:
    try:
        x = float(x)
        return x
    except Exception:
        return 0.0
