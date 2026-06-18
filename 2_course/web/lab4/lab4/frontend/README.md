# 🎯 Point-in-Area Checker Frontend

> **React + Redux Toolkit фронтенд**

![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

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
