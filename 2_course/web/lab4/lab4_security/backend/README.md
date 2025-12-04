# 🎯 Point-in-Area Checker Backend

> **REST API на Spring Boot бэкенд с PostgreSQL**

[![Java](https://img.shields.io/badge/Java-17+-blue.svg)](https://www.java.com/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-4.0.0-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Gradle](https://img.shields.io/badge/Gradle-8-brightgreen.svg)](https://gradle.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

## Стек

### Backend
- **Java 17**
- **Gradle**
- **Spring Boot 4.0.0**
- **Spring Boot DevTools**, **Spring Web MVC**, **Spring Security**, **Validation**, **Lombok**
- **Spring Data JPA**, **JDBC PostgreSQL**
- **PostgreSQL**

## Аутентификация (Principal/Credential/Evidence)
- Principal: пользователь с UUID и логином.
- Credential: способы входа (пароль, 5 одноразовых recovery-кодов, право владения файлом).
- Evidence: проверка существования на устройстве файла, содержащего сгенерированный токен, соответствующий аккаунту.

## Структура проекта

```
backend/
├── build/
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
│       │   │   ├── credential/
│       │   │   │   ├── CredentialEntity.java
│       │   │   │   ├── CredentialRepository.java
│       │   │   │   ├── CredentialType.java
│       │   │   │   ├── CredentialVerifier.java
│       │   │   │   ├── OwnershipCredentialVerifier.java
│       │   │   │   ├── PasswordCredentialVerifier.java
│       │   │   │   └── RecoveryCredentialVerifier.java
│       │   │   ├── principal/
│       │   │   │   ├── PrincipalEntity.java
│       │   │   │   └── PrincipalRepository.java
│       │   │   └── dto/
│       │   │       ├── CredentialResponse.java
│       │   │       ├── LoginRequest.java
│       │   │       ├── LoginResponse.java
│       │   │       ├── PasswordRequest.java
│       │   │       ├── RegisterRequest.java
│       │   │       ├── RegisterResponse.java
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
