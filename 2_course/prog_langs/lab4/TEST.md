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
# Сборка (из корневой папки)
dotnet run --project cs_compute

# Запуск (в новом терминале)
cd python_app
python main.py
```

---

## macOS

```bash
# Подготовка тестовых программ
# Сборка (из корневой папки)
dotnet run --project cs_compute

# Запуск (в новом терминале)
cd python_app
python main.py
```
