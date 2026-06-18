# 🎯 Лабораторная работа №2

> **Веб-приложение, проверяющее попадание точки в область и прогнозирующее шанс попадания через логистическую регрессию**

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

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
