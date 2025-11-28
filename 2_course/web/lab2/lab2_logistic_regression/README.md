# 🎯 Point-in-Area + LogReg

> **Веб-приложение, проверяющее попадание точки в область и прогнозирующее шанс попадания через логистическую регрессию**

[![Java](https://img.shields.io/badge/Java-17+-blue.svg)](https://www.java.com/)
[![Gradle](https://img.shields.io/badge/Gradle-8+-brightgreen.svg)](https://gradle.org)
[![Tribuo](https://img.shields.io/badge/Tribuo-4.3.2-orange.svg)](https://tribuo.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://javascript.info)

## 📋 Описание проекта

Веб-приложение на сервлетах и JSP с интерактивным графиком, позволяющее проверить попадание точки в сложную область при выбранном R. Координаты задаются из формы или кликом по графику, результаты фиксируются в таблице и складируются в CSV. Логистическая регрессия автоматически обучается на накопленных попаданиях/промахах и показывает вероятность успеха перед отправкой следующего запроса.

**Реализация:**
- Проверка принадлежности к составной области 
- Сохранение истории запросов в памяти и CSV
- Автоматическое дообучение логистической регрессии Tribuo и предсказание вероятности попадания
- JSP-интерфейс с таблицей результатов и подсветкой попаданий/промахов

## Стек

### Backend
- **Java 17**
- **Gradle**
- **Jakarta Servlet / JSP 6**
- **Jakarta CDI / Inject**
- **JSTL 3.0**
- **Tribuo (LogisticRegressionTrainer)**

### Frontend  
- **Vanilla JavaScript (ES6+)**
- **HTML5 Canvas**
- **CSS3**

## Структура проекта

```
lab2_logistic_regression/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/
├── build/
├── src/
│   └── main/
│       ├── java/
│       │   └── org/example/
│       │       ├── ml/
│       │       │   └── ModelManager.java
│       │       ├── model/
│       │       │   ├── AreaChecker.java
│       │       │   ├── Params.java
│       │       │   ├── Result.java
│       │       │   ├── ResultsBean.java
│       │       │   └── ValidationException.java
│       │       └── servlets/
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
└── README.md
```
