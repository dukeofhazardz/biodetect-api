# Helper Functions
import re

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

def parse_response_to_json(response):
    res_json = {}
    try:
        split_data = re.split(r'[0-9]\.\s', response)
        print(split_data)
        for data in split_data[1:]:
            section = re.split(":", data)
            print(section)
            if len(section) == 2:
                key = section[0].lower()
                value = section[1].strip('\n1')
                res_json[key] = value
    except Exception as e:
        res_json["error"] = "Not an image of a living organism (plant, insect or animal)"
    finally:
        return res_json