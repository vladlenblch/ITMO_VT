import re
import json


def parse(json_data):
    yaml_data = ""

    def parse_dict(d, num_spaces=0):
        nonlocal yaml_data
        for key, value in d.items():
            if isinstance(value, dict):
                yaml_data += f"{' ' * num_spaces}{key}:\n"
                parse_dict(value, num_spaces + 2)
            elif isinstance(value, list):
                yaml_data += f"{' ' * num_spaces}{key}:\n"
                parse_list(value, num_spaces + 2)
            else:
                formatted_value = parse_value(value)
                yaml_data += f"{' ' * num_spaces}{key}: {formatted_value}\n"

    def parse_list(l, num_spaces = 0):
        nonlocal yaml_data
        for item in l:
            if isinstance(item, dict):
                yaml_data += f"{' ' * (num_spaces - 2)}- "
                parse_dict(item, num_spaces + 2)
            elif isinstance(item, list):
                yaml_data += f"{' ' * (num_spaces - 2)}- "
                parse_list(item, num_spaces + 2)
            else:
                parsed_item = parse_value(item)
                yaml_data += f"{' ' * (num_spaces - 2)}- {parsed_item}\n"

    def parse_value(value):
        if isinstance(value, str):
            if value == "":
                return "''"
            if re.match(r'^\d{1,2}:[0-5]\d$', value):
                return f"'{value}'"
        return value

    if isinstance(json_data, dict):
        parse_dict(json_data)
    elif isinstance(json_data, list):
        parse_list(json_data)
    return yaml_data


with open('D:\ITMO\informatics\лаба 4\schedule.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)
yaml_result = parse(json_data)

with open('D:\ITMO\informatics\лаба 4\out2.yaml', "w", encoding='utf-8') as file:
    file.write(yaml_result)
