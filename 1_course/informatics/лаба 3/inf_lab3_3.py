import re
import re
import json

test = input()
pattern = r"^(0?[0-9]|[1-5]\d|\*)\s+(0?[0-9]|1\d|2[0-3]|\*)\s+(0?[1-9]|[12][0-9]|3[01]|\*)\s+(0?[1-9]|1[0-2]|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\*)\s+(0?[0-6]|sun|mon|tue|wed|thu|fri|sat|\*)$"
ans = re.match(pattern, test)

my_answers = []
if ans:
    my_answers.append('Correct!')
    print('Correct!')
else:
    my_answers.append('Fail!')
    print('Fail!')

my_json = {}
my_json["answers"] = my_answers
with open('result.json', 'w', encoding="utf-8") as file:
    dumped_json = json.dumps(my_json, ensure_ascii=False)
    file.write(dumped_json)
