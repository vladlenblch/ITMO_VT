# 🎯 Лабораторная работа №3.3

![Assembly](https://img.shields.io/badge/Assembly-6E4C13?style=flat&logo=assemblyscript&logoColor=white)

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: rle_decompress_bytes

```python
def rle_decompress_bytes(*input_words):
    """Run-length decompression for bytes packed in 32-bit words.

    Input format:
    - First word: length of compressed data in bytes
    - Following words: compressed data as count+byte pairs

    Output format:
    - First word: length of decompressed data in bytes
    - Following words: decompressed bytes packed in words

    Example: [2, 0x040A0000] -> [4, 0x0A0A0A0A] (count=4, byte=0x0A -> 4 bytes of 0x0A)
    """
    if not input_words:
        return [-1]

    length = input_words[0]
    if length < 0:
        return [-1]

    if length == 0:
        return [0]

    if length % 2 != 0:
        return [-1]  # Compressed data must be count+byte pairs

    try:
        # Extract compressed bytes from words
        compressed_data = []
        word_count = (length + 3) // 4  # Round up to nearest word

        for i in range(1, min(len(input_words), word_count + 1)):
            word = input_words[i]
            for j in range(4):
                if len(compressed_data) < length:
                    byte_val = (word >> (24 - j * 8)) & 0xFF
                    compressed_data.append(byte_val)

        if len(compressed_data) < length:
            return [-1]  # Not enough input data

        # Decompress bytes
        decompressed = []
        for i in range(0, len(compressed_data), 2):
            if i + 1 >= len(compressed_data):
                return [-1]  # Invalid format

            count = compressed_data[i]
            byte_val = compressed_data[i + 1]

            if count == 0:
                return [-1]  # Invalid count

            decompressed.extend([byte_val] * count)

        # Pack decompressed data into words
        result = [len(decompressed)]  # Length in bytes

        for i in range(0, len(decompressed), 4):
            word = 0
            for j in range(4):
                if i + j < len(decompressed):
                    word |= (decompressed[i + j] & 0xFF) << (24 - j * 8)
            result.append(word)

        return result

    except Exception:
        return [-1]


assert rle_decompress_bytes([2, 67764224]) == [4, 168430090]
assert rle_decompress_bytes([6, 44696251, 80478208]) == [8, 2863315899, 3435973836]
assert rle_decompress_bytes([2, 33488896]) == [1, 4278190080]
```
