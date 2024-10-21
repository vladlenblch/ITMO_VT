import re

test = input()
pattern = r"=-\\"
print(len(re.findall(pattern, test)))
