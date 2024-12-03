import json
import yaml

def parse(json_file_path, yaml_file_path):
    with open('D:\ITMO\informatics\лаба 4\schedule.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('D:\ITMO\informatics\лаба 4\out1.yaml', 'w', encoding='utf-8') as yaml_file:
        yaml.dump(data, yaml_file, allow_unicode=True, default_flow_style=False)


parse('schedule.json', 'out1.yaml')
