# 🎯 Лабораторная работа №3.6

![Assembly](https://img.shields.io/badge/Assembly-6E4C13?style=flat&logo=assemblyscript&logoColor=white)

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: fnv32_1_hash

```python
def fnv32_1_hash(xs):
    """Input: stream of chars forming c string style (end with 0)

    Need to calculate FNV-1 32 bit hash of input string
    More info: https://ru.wikipedia.org/wiki/FNV
    """
    it = 0
    fnv32_prime = 0x01000193
    hash_value = 0x811C9DC5
    while ord(xs[it]) > 0:
        hash_value = (hash_value * fnv32_prime) & 0xFFFFFFFF
        hash_value ^= ord(xs[it])
        it += 1

    return hash_value


assert fnv32_1_hash('a\0') == 84696446
assert fnv32_1_hash('abc\0') == 1134309195
assert fnv32_1_hash('Computers are awesome!\0') == 3917207935
```
