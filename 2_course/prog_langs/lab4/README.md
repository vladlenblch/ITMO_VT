# 🎯 Лабораторная работа №4

> **Потоковая визуализация фрактала Коллатца: C# генерирует кадры, Python отображает с FPS**

![C#](https://img.shields.io/badge/C%23-239120?style=flat&logo=csharp&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

## 📋 Описание проекта

Консольное приложение на C# генерирует фрактал Коллатца и стримит байтовую карту итераций по TCP на `localhost:5001`. Python‑клиент принимает поток, визуализирует фрактал и приближает его.

## 👤 Автор

- Ларионов Владислав Васильевич  
- Группа: P3209  
- Вариант: Collatz fractal, CPython -> C#

## Стек

### Core
- **C# (.NET 8.0)**
- **Python 3**
- **NumPy**
- **pygame**

## Структура проекта

```
lab4/
├── cs_compute/
│   ├── Program.cs
│   └── Compute.csproj
├── python_app/
│   ├── main.py
│   └── requirements.txt
├── .gitignore
└── README.md
```
