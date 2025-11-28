# 🎯 Point-in-Area + RL Agent

> **Веб-приложение на JSF, проверяющее попадание точки в область и получающее рекомендуемый радиус от агента обучения с подкреплением через Kafka**

[![Java](https://img.shields.io/badge/Java-17-blue.svg)](https://www.java.com/)
[![Gradle](https://img.shields.io/badge/Gradle-8-brightgreen.svg)](https://gradle.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Kafka](https://img.shields.io/badge/Kafka-3.7.0-black.svg)](https://kafka.apache.org)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)

## 📋 Описание проекта

JSF-приложение c PrimeFaces отображает интерактивный график и форму, принимает координаты кликом или вводом и сохраняет результат в PostgreSQL. Каждые пять запросов бэкенд отправляет в Kafka статистику последних десяти попаданий, а отдельный Python-агент с Q-learning (Reinforcement Learning) принимает решение, как скорректировать радиус R и публикует новое значение обратно. UI берет рекомендацию, показывает текущую нагрузку на БД.

**Реализация:**
- Хранение истории запросов в PostgreSQL, метрика запросов в минуту
- Kafka-интеграция: отправка состояния, приём действия с новым R
- PrimeFaces компоненты
- Python-агент: Q-таблица, epsilon-greedy policy, расчёт награды и отправка действий

## Стек

### Backend
- **Java 17**
- **Gradle 8**
- **Jakarta Faces**
- **PrimeFaces 13 (jakarta)**
- **PostgreSQL** через JDBC
- **Kafka clients 3.7 + Jackson**

### Frontend  
- **JSF (Facelets)**
- **PrimeFaces**
- **Vanilla JavaScript (ES6+)**
- **CSS3**

### Python agent
- **Python 3.11+**
- **kafka-python**
- **dataclasses-json**

## Структура проекта

Веб-приложение:
```
lab3_reinforcement_learning/
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
│       │       │   └── ResultsBean.java
│       │       ├── entities
|       |       |   └── PointEntity.java
│       │       ├── service/
│       │       │   ├── DatabaseService.java
│       │       │   └── KafkaService.java
│       │       └── validation/
│       │           ├── RValidator.java
│       │           ├── XValidator.java
│       │           └── YValidator.java
│       ├── resources/
|       |   └── db.cfg
│       └── webapp/
│           ├── index.xhtml
│           ├── form.xhtml
│           ├── graph.js
│           ├── style.css
│           └── WEB-INF/
│               ├── beans.xml
│               ├── faces-config.xml
│               └── web.xml
└── README.md
```

RL-агент:
```
rl-agent/
├── main.py
├── agent.py
├── kafka_io.py
├── reward.py
├── state.py
└── requirements.txt
```
