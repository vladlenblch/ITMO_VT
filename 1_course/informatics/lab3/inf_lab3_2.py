import re
import json

test = input()
pattern = r"(?<![:а-яА-Я0-10])([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?\b(?![:а-яА-Я])"
ans = re.sub(pattern, '(TBD)', test)

my_json = {}
my_answers = [ans]
my_json["answers"] = my_answers
with open('result.json', 'w', encoding="utf-8") as file:
    dumped_json = json.dumps(my_json, ensure_ascii=False)
    file.write(dumped_json)
