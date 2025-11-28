# 🎯 Point-in-Area Checker Frontend

> **React + Redux Toolkit фронтенд**

[![React](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev)
[![Redux Toolkit](https://img.shields.io/badge/Redux%20Toolkit-State-orange.svg)](https://redux-toolkit.js.org/)
[![Axios](https://img.shields.io/badge/Axios-HTTP-purple.svg)](https://axios-http.com/)

## Стек

### Frontend
- **React 19 (CRA)**
- **Redux Toolkit**
- **React Router DOM 7**
- **Axios**
- **CSS** 

## Структура проекта

```
frontend/
├── build/
├── node_modules/
├── package.json
├── package-lock.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.js
│   ├── app/
│   │   └── store.js
│   ├── features/
│   │   ├── auth/
│   │   │   └── authSlice.js
│   │   └── points/
│   │       └── pointsSlice.js
│   ├── services/
│   │   ├── apiClient.js
│   │   ├── authApi.js
│   │   └── pointsApi.js
│   ├── routes/
│   │   └── ProtectedRoute.jsx
│   ├── pages/
│   │   ├── LandingPage.css
│   │   ├── LandingPage.jsx
│   │   ├── MainPage.css
│   │   └── MainPage.jsx
│   └── components/
│       ├── AreaChart.css
│       ├── AreaChart.jsx
│       ├── Header.css
│       ├── Header.jsx
│       ├── LoginForm.css
│       ├── LoginForm.jsx
│       ├── LogoutButton.css
│       ├── LogoutButton.jsx
│       ├── PointControls.css
│       ├── PointControls.jsx
│       ├── ResultsTable.css
│       └── ResultsTable.jsx
└── README.md
```
