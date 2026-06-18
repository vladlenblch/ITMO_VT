# 🎯 Лабораторная работа №1

> **Система отслеживания взгляда с веб-интерфейсом для проверки попадания точки в заданную область**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-4285F4?style=flat&logo=google&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

## 📋 Описание проекта

Веб-приложение, которое в реальном времени отслеживает направление взгляда пользователя через веб-камеру и определяет попадание точки взгляда в заранее заданную область на графике. Выстрел осуществляется по нажатию на пробел.

**Реализация:**
- Отслеживание взгляда в реальном времени
- Визуализация точки взгляда на графике в реальном времени
- Проверка попадания в сложную, заранее заданную геометрическую область
- WebSocket соединение для мгновенной передачи данных
- История результатов с временными метками хранится в таблице под графиком

## Стек

### Backend
- **FastAPI**
- **WebSocket Server**
- **OpenCV + MediaPipe**
- **Uvicorn**

### Frontend  
- **Vanilla JavaScript (ES6+)**
- **HTML5 Canvas**
- **CSS3**
- **WebSocket API**

## Структура проекта

```
lab1_eyetracker_app/
├── main.py
├── integrated_server.py
├── eye_tracker.py
├── requirements.txt
├── README.md
└── static/
    ├── index.html
    ├── styles.css
    └── index.js
```
