import json


def reformat(lines):
    if isinstance(lines, list):
        lines = ''.join(lines)

    try:
        json_obj = json.loads(lines)
    except json.JSONDecodeError as e:
        raise ValueError(f"ошибка: {e}")

    def reformat_lists(obj):
        if isinstance(obj, list):
            return f"[{', '.join(json.dumps(item, ensure_ascii=False) for item in obj)}]"
        elif isinstance(obj, dict):
            return {k: reformat_lists(v) for k, v in obj.items()}
        else:
            return obj

    formatted_obj = reformat_lists(json_obj)

    formatted_json = json.dumps(formatted_obj, indent=2, ensure_ascii=False, separators=(', ', ': '))

    return formatted_json.splitlines()


def rmv(lines):
    lines = [ln for ln in lines if ln.strip()]
    if lines:
        num = len(lines[0]) - len(lines[0].strip())
        lines = [ln.replace(" " * num, "", 1) for ln in lines]
    return lines


def parse_quotmarks(s):
    if ':' in s:
        s = s.replace("\"", "", 1).replace("\":", ":")
    if not any((i + ":") in s for i in '0123456789') and not ("\"\"" in s):
        s = s.replace("\",", "").replace("\"", "")
    else:
        s = s.replace("\",", "\'").replace("\"", "\'")
    if "\"," in s:
        s = s.replace("\",", "\"")
    return s


def parse_arr(s):
    if "[" in s:
        num_spaces = len(s) - len(s.strip())
        s = s.replace("]", "")
        s = s.replace(" [", "\n" + " " * num_spaces + "- ")
        s = s.replace(", ", "\n" + " " * num_spaces + "- ")
    return s


with open('D:\ITMO\informatics\лаба 4\schedule.json', "r", encoding='utf-8') as file:
    lines = file.readlines()

formatted_lines = reformat(lines)

for i in range(len(formatted_lines)):
    formatted_lines[i] = formatted_lines[i].replace('},', '').replace('}', '').replace(' {', '').replace('{','').replace('\n', '')
    formatted_lines[i] = parse_quotmarks(formatted_lines[i])
    formatted_lines[i] = parse_arr(formatted_lines[i])

formatted_lines = rmv(formatted_lines)

with open('D:\ITMO\informatics\лаба 4\out.yaml', "w", encoding='utf-8') as file:
    for ln in formatted_lines:
        file.write(ln.replace('    ', '  ') + '\n')
