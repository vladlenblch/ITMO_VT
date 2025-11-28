# 🎯 Point-in-Area Checker

> **Java + PrimeFaces веб-приложение для проверки попадания точки в область и сохранения результатов в БД**

[![Java](https://img.shields.io/badge/Java-17+-blue.svg)](https://www.java.com/)
[![Gradle](https://img.shields.io/badge/Gradle-8-brightgreen.svg)](https://gradle.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://javascript.info)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

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
├── src/
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
└── build/
```
