# 🎯 Лабораторная работа №3.1

![Assembly](https://img.shields.io/badge/Assembly-6E4C13?style=flat&logo=assemblyscript&logoColor=white)

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: count_leading_zeros

```python
def count_leading_zeros(n):
    """Count the number of leading zeros in the binary representation of an integer.

    Args:
        n (int): The integer to count leading zeros for.

    Returns:
        int: The number of leading zeros.
    """
    if n == 0:
        return 32
    count = 0
    for i in range(31, -1, -1):
        if (n >> i) & 1 == 0:
            count += 1
        else:
            break
    return count


assert count_leading_zeros(1) == 31
assert count_leading_zeros(2) == 30
assert count_leading_zeros(16) == 27
```
