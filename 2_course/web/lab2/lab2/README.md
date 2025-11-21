# 🎯 Point-in-Area Checker

> **Java + JavaScript веб-приложение для проверки попадания точки в область на плоскости**

[![Java](https://img.shields.io/badge/Java-17+-blue.svg)](https://www.java.com/)
[![Maven](https://img.shields.io/badge/Maven-3+-blueviolet.svg)](https://maven.apache.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://javascript.info)

## 📋 Описание проекта

Интерактивное веб-приложение, позволяющее пользователю проверить, попадает ли точка с координатами в заданную область. Ввод осуществляется через форму, либо нажатием на сам график, результат отображается в таблице и на графике.

## 👤 Автор

- Ларионов Владислав Васильевич
- Группа: P3209
- Вариант: 745

## Стек

### Backend
- **Java 17+**
- **Maven (WAR packaging)**
- **Jakarta Servlet / JSP**
- **Jakarta CDI (Weld / контейнерная реализация в WildFly)**

### Frontend
- **Vanilla JavaScript (ES6+)**
- **HTML5 Canvas**
- **CSS3**

## Структура проекта

```
lab2/
├── pom.xml
├── README.md
├── src/
│   └── main/
│       ├── java/
│       │   └── org/example/
│       │       ├── model/
│       │       │   ├── AreaChecker.java
│       │       │   ├── Params.java
│       │       │   ├── Result.java
│       │       │   ├── ResultsBean.java
│       │       │   └── ValidationException.java
│       │       └── servlets/
│       │           ├── AppContextListener.java
│       │           ├── ControllerServlet.java
│       │           ├── AreaCheckServlet.java
│       │           └── ResultServlet.java
│       └── webapp/
│           ├── form.jsp
│           ├── result.jsp
│           ├── index.js
│           ├── style.css
│           └── WEB-INF/
│               ├── web.xml
│               └── beans.xml
└── target/
```
