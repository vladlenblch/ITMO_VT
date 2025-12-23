# 🎯 Лабораторная работа №5

> **Интерактивный REPL целочисленных выражений: Shunting Yard → AST → вычисление**

![C#](https://img.shields.io/badge/C%23-.NET%208.0-239120?style=for-the-badge&logo=c-sharp)
![.NET](https://img.shields.io/badge/.NET-8.0-512BD4?style=for-the-badge&logo=dotnet)
![x86-64](https://img.shields.io/badge/64--bit-integers-000000?style=for-the-badge)

## 📋 Описание проекта

Консольное приложение на C# разбирает арифметические выражения в инфиксной форме, строит обратную польскую запись (Shunting Yard) и AST, затем интерпретирует её. Команда `do` вычисляет в 64-битных целых, выводит каждое подвыражение и итоговый результат.

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
