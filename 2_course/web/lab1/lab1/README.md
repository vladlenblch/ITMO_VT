# 🎯 Point-in-Area Checker

> **Java + JavaScript веб-приложение для проверки попадания точки в область на плоскости**

[![Java](https://img.shields.io/badge/Java-17+-blue.svg)](https://www.java.com/)
[![Gradle](https://img.shields.io/badge/Gradle-8+-green.svg)](https://gradle.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://javascript.info)

## 📋 Описание проекта

Интерактивное веб-приложение, позволяющее пользователю проверить, попадает ли точка с координатами (X, Y) в заданную область. Ввод осуществляется через форму, результат отображается в таблице и на графике.

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
- **Responsive Design**

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
└── README.MD
```
