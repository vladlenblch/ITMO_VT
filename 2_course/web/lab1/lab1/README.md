# 🎯 Лабораторная работа №1

> **Java + JavaScript веб-приложение для проверки попадания точки в область на плоскости**

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

## 📋 Описание проекта

Интерактивное веб-приложение, позволяющее пользователю проверить, попадает ли точка с координатами в заданную область. Ввод осуществляется через форму, результат отображается в таблице и на графике.

## 👤 Автор

- Ларионов Владислав Васильевич  
- Группа: P3209  
- Вариант: 466468

## Стек

### Backend
- **Java 17+**
- **Gradle**
- **FastCGI (через fastcgi-lib.jar)**

### Frontend
- **Vanilla JavaScript (ES6+)**
- **HTML5 Canvas**
- **CSS3**

## Структура проекта

```
lab1/
├── build.gradle
├── gradlew / gradlew.bat
├── libs/
│   └── fastcgi-lib.jar
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── org/example/
│   │   │       ├── Main.java
│   │   │       ├── Params.java
│   │   │       └── ValidationException.java
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
├── static/
│   ├── index.html
│   └── index.js
└── README.md
```
