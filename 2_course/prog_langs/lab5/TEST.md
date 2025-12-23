# Инструкция по тестированию проекта

## Требования

**Windows:**
- .NET SDK 8.0+
- Поддержка x64 (кодогенерация под Intel/AMD)

**macOS:**
- .NET SDK 8.0+
- Поддержка x64 (кодогенерация под Intel/AMD)

---

## Windows

```powershell
# Сборка и запуск (из корневой папки)
dotnet run --project Lab5.csproj

# Пример сессии
# expr x+y*(10-z)/2
# set x 5
# set y 10
# set z 6
# do
```

---

## macOS

```bash
# Сборка и запуск (из корневой папки)
dotnet run --project Lab5.csproj

# Пример сессии
# expr x+y*(10-z)/2
# set x 5
# set y 10
# set z 6
# do
```
