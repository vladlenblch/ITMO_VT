import json


def parse(json_obj, num_spaces=0):
    yaml_str = ""

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key.startswith("#"):
                yaml_str += ' ' * num_spaces + f"'{key}': "
            else:
                yaml_str += ' ' * num_spaces + f"{key}: "
            if isinstance(value, (dict, list)):
                yaml_str += "\n" + parse(value, num_spaces + 2)
            else:
                yaml_str += f"{parse(value, 0).strip()}\n"

    elif isinstance(json_obj, list):
        for item in json_obj:
            if isinstance(item, list):
                yaml_str += ' ' * (num_spaces - 2) + "- " + parse(item, num_spaces + 2).strip() + "\n"
            else:
                yaml_str += ' ' * (num_spaces - 2) + f"- {parse(item, num_spaces).strip()}\n"

    elif isinstance(json_obj, bool):
        if json_obj:
            yaml_str += "true"
        else:
            yaml_str += "false"

    elif json_obj is None:
        yaml_str += ""

    elif isinstance(json_obj, str):
        if json_obj == "":
            yaml_str += "''"
        elif any((i + ":") in json_obj for i in '0123456789'):
            yaml_str += f"'{json_obj}'"
        elif json_obj == "'":
            yaml_str += json_obj.replace("'", "'\\''")
        elif json_obj == "\"":
            yaml_str += json_obj.replace("\"", "'\\\"'")
        elif json_obj == "/" or json_obj == "\\":
            yaml_str += json_obj.replace("/", "'/'").replace("\\", "'\\\\'")
        elif json_obj == "\n" or json_obj == "\t" or json_obj == "\r" or json_obj == "\f" or json_obj == "\b":
            yaml_str += json_obj.replace("\n", "'\\n'").replace("\t", "'\\t'").replace("\r", "'\\r'").replace("\f", "'\\f'").replace("\b", "'\\b'")
        elif "\n" in json_obj or "\t" in json_obj or "\r" in json_obj or "\f" in json_obj or "\b" in json_obj:
            yaml_str += json_obj.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\f", "\\f").replace("\b", "\\b")
        elif len(json_obj) == 1 and ord(json_obj) > 127:
            yaml_str += "'" + json_obj + "'"
        elif json_obj.startswith("#"):
            yaml_str += f"'{json_obj}'"
        else:
            yaml_str += json_obj

    else:
        yaml_str += str(json_obj)

    return yaml_str


with open('D:\ITMO\informatics\лаба 4\schedule.json.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)
yaml_data = parse(json_data)

with open('D:\ITMO\informatics\лаба 4\out3.yaml', 'w', encoding='utf-8') as file:
    file.write(yaml_data)
