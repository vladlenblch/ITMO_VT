# 🎯 Лабораторная работа №3.4

![Assembly](https://img.shields.io/badge/Assembly-6E4C13?style=flat&logo=assemblyscript&logoColor=white)

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: sum_of_digits

```python
def sum_of_digits(n):
    """Calculate the sum of the digits of a number"""
    total = 0
    n = abs(n)
    while n > 0:
        total += n % 10
        n //= 10
    return total


assert sum_of_digits(123) == 6
assert sum_of_digits(-456) == 15
```
