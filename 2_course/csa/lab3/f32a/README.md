# 🎯 Лабораторная работа №3.2

![Assembly](https://img.shields.io/badge/Assembly-6E4C13?style=flat&logo=assemblyscript&logoColor=white)

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: upper_case_cstr

```python
def upper_case_cstr(s):
    """Convert a C string to upper case.

    - Result string should be represented as a correct C string.
    - Buffer size for the message -- `0x20`, starts from `0x00`.
    - End of input -- new line.
    - Initial buffer values -- `_`.

    Python example args:
        s (str): The input C string.

    Returns:
        tuple: A tuple containing the upper case string and an empty string.
    """
    line, rest = read_line(s, 0x20)
    if line is None:
        return [overflow_error_value], rest
    return cstr(line.upper(), 0x20)[0], rest


assert upper_case_cstr('Hello\n') == ('HELLO', '')
# and mem[0..31]: 48 45 4c 4c 4f 00 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f
assert upper_case_cstr('world\n') == ('WORLD', '')
# and mem[0..31]: 57 4f 52 4c 44 00 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f
```
