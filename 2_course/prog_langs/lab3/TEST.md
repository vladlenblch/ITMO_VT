# Инструкция по тестированию проекта

## Требования

**Windows:**
- .NET SDK 8.0+
- gcc/g++ (MinGW или Visual Studio Build Tools)

**macOS:**
- .NET SDK 8.0+
- gcc/g++ (Xcode Command Line Tools)

---

## Windows

```powershell
# Подготовка тестовых программ
gcc -o test_c.exe test_c.c
g++ -o test_cpp.exe test_cpp.cpp

# Сборка
dotnet build

# Запуск
dotnet run -- .\test_c.exe .\test.sh .\test_cpp.exe
```

---

## macOS

```bash
# Подготовка тестовых программ
gcc -o test_c test_c.c
g++ -o test_cpp test_cpp.cpp
chmod +x test.sh

# Сборка
dotnet build

# Запуск
dotnet run -- ./test_c ./test.sh ./test_cpp
```
