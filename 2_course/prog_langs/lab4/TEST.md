# Инструкция по тестированию проекта

## Требования

**Windows:**
- .NET SDK 8.0+
- gcc/g++ (MinGW или Visual Studio Build Tools)
- Python 3.12+

**macOS:**
- .NET SDK 8.0+
- gcc/g++ (Xcode Command Line Tools)
- Python 3.12+

---

## Windows

```powershell
# Сборка (из корневой папки)
dotnet run --project cs_compute

# Запуск (в новом терминале)
cd python_app
python main.py
```

---

## macOS

```bash
# Сборка (из корневой папки)
dotnet run --project cs_compute

# Запуск (в новом терминале)
cd python_app
python main.py
```
