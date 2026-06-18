# 🎯 Point-in-Area Checker Backend

> **REST API-бэкенд на Spring Boot с PostgreSQL**

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat&logo=springboot&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)

## Стек

### Backend
- **Java 17**
- **Gradle**
- **Spring Boot 4.0.0**
- **Spring Boot DevTools**, **Spring Web MVC**, **Spring Security**, **Validation**, **Lombok**
- **Spring Data JPA**, **JDBC PostgreSQL**
- **PostgreSQL**

## Структура проекта

```
backend/
├── build.gradle.kts
├── gradle.properties
├── settings.gradle.kts
├── gradlew
├── gradlew.bat
├── gradle/
├── src/
│   └── main/
│       ├── java/ru/vladlenblch/
│       │   ├── BackendApplication.java
│       │   ├── config/
│       │   │   └── SecurityConfig.java
│       │   ├── auth/
│       │   │   ├── AuthController.java
│       │   │   ├── AuthService.java
│       │   │   ├── UserEntity.java
│       │   │   ├── UserRepository.java
│       │   │   └── dto/
│       │   │       ├── LoginRequest.java
│       │   │       ├── LoginResponse.java
│       │   │       ├── RegisterRequest.java
│       │   │       └── UserDto.java
│       │   └── points/
│       │       ├── PointEntity.java
│       │       ├── PointsController.java
│       │       ├── PointsRepository.java
│       │       ├── PointsService.java
│       │       └── dto/
│       │           ├── PointRequest.java
│       │           └── PointResponse.java
│       └── resources/
│           └── application.properties
└── README.md
```
