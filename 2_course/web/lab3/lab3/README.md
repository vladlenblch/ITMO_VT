# 🎯 Лабораторная работа №3

> **Java + PrimeFaces веб-приложение для проверки попадания точки в область и сохранения результатов в БД**

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

## 📋 Описание проекта

Веб-приложение на JSF и PrimeFaces: пользователь задает координаты точки и радиус, либо кликает по интерактивному графику. Попадание рассчитывается на бэкенде, результат с временными метками сохраняется в PostgreSQL, а история пользователя обновляется через AJAX.

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: 613

## Стек

### Backend
- **Java 17**
- **Gradle**
- **Jakarta Faces 3.0 + PrimeFaces 13 (Jakarta)**
- **Jakarta Servlet 5 / CDI / Bean Validation**
- **JDBC + PostgreSQL**

### Frontend
- **PrimeFaces UI + Facelets (XHTML)**
- **Vanilla JavaScript (ES6)**
- **CSS3**

## Структура проекта

```
lab3/
├── build.gradle.kts
├── gradle.properties
├── settings.gradle.kts
└── src/
│   └── main/
│       ├── java/
│       │   └── org/example/
│       │       ├── beans/
│       │       │   ├── ClockBean.java
│       │       │   ├── PointBean.java
│       │       │   ├── ResultsBean.java
│       │       │   └── UserBean.java
│       │       ├── entities/
│       │       │   ├── PointEntity.java
│       │       │   └── UserEntity.java
│       │       ├── service/
│       │       │   └── DatabaseService.java
│       │       └── validation/
│       │           ├── RValidator.java
│       │           ├── XValidator.java
│       │           └── YValidator.java
│       ├── resources/
│       │   └── db.cfg
│       └── webapp/
│           ├── form.xhtml
│           ├── graph.js
│           ├── index.xhtml
│           ├── style.css
│           └── WEB-INF/
│               ├── beans.xml
│               ├── faces-config.xml
│               └── web.xml
```
