# 🎯 Лабораторная работа №5

> **Интерактивный REPL целочисленных выражений: Shunting Yard → AST → вычисление**

![C#](https://img.shields.io/badge/C%23-239120?style=flat&logo=csharp&logoColor=white)

## 📋 Описание проекта

Консольное приложение на C# разбирает арифметические выражения в инфиксной форме, строит обратную польскую запись (Shunting Yard) и AST, затем интерпретирует ее. Команда `do` вычисляет в 64-битных целых, выводит каждое подвыражение и итоговый результат.

## 👤 Автор

- Ларионов Владислав Васильевич  
- Группа: P3209  
- Вариант: 7 (Shunting Yard + OpCodes)

## Стек

### Core
- **C# (.NET 8.0)**
- **Shunting Yard + AST интерпретатор**

## Структура проекта

```
lab5/
├── Lab5.csproj
├── Program.cs
├── Interpreter.cs
├── Tokenizer.cs
├── Parser.cs
├── Nodes.cs
├── README.md
└── TEST.md
```
