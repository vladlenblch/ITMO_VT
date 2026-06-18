# 🎯 Лабораторная работа №3

> **C# приложение для параллельного запуска программ в фоновом режиме с хронологическим выводом stdout**

![C#](https://img.shields.io/badge/C%23-239120?style=flat&logo=csharp&logoColor=white)

## 📋 Описание проекта

Консольное приложение на языке C# для параллельного запуска нескольких программ в фоновом режиме. Принимает пути к программам в качестве аргументов командной строки, запускает их асинхронно используя Task, перехватывает их stdout и выводит данные в хронологическом порядке появления.

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209  
- Вариант: Task-based program launcher with chronological output

## Стек

### Core
- **C# (.NET 8.0)**
- **Task и async/await**
- **ConcurrentQueue**
- **Process**

## Структура проекта

```
lab3/
├── Program.cs
├── lab3.csproj
├── test_c.c
├── test_cpp.cpp
├── test.sh
├── test_c
├── test_cpp
├── .gitignore
├── TEST.md
└── README.md
```
