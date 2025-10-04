# 🎯 EyeTracker

> **Система отслеживания взгляда с веб-интерфейсом для проверки попадания точки в заданную область**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://javascript.info)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)](https://mediapipe.dev)

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
├── README.MD
└── static/
    ├── index.html
    ├── styles.css
    └── index.js
```
