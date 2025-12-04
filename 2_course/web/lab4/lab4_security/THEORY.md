# Полное описание архитектуры и изменений

Документ перечисляет все ключевые решения в проекте, охватывает бэкенд и фронтенд, подробно описывает валидацию, модель Principal/Credential/Evidence, способы входа (пароль, recovery-коды, право владения файлом), стратегии (CDI/Spring бины), сущности, эндпоинты, логику, генерацию кодов, поток данных и расположение файлов. Отдельно указано, что FIDO2/WebAuthn в текущей версии не реализованы.

## Общая структура репозитория
1. Корень: `README.md`, `THEORY.md` (этот файл).
2. Бэкенд: `backend/` (Spring Boot, Java 17, Gradle).
3. Фронтенд: `frontend/` (React 19, Redux Toolkit, React Router DOM, Zod для валидации).
4. Данные права владения: создаются при регистрации в `backend/data/ownership/<login>.txt`.

## Бэкенд: обзор
1. Основной пакет: `ru.vladlenblch`.
2. Запуск: `backend/src/main/java/ru/vladlenblch/BackendApplication.java`.
3. Конфигурация безопасности: `config/SecurityConfig.java` — CORS, отключённый CSRF, разрешены все запросы кроме логина (который тоже permitAll).
4. Логика аутентификации: пакет `auth/`.
5. Точки: пакет `points/` — хранение и проверка попадания точек, привязано к Principal.

## Бэкенд: модель Principal/Credential/Evidence
1. Principal
   - Класс: `auth/principal/PrincipalEntity.java`.
   - Поля: `UUID id`, `String username`, `Instant createdAt`.
   - Таблица: `principals`.
   - Репозиторий: `auth/principal/PrincipalRepository.java` (`findByUsername`).
2. Credential
   - Класс: `auth/credential/CredentialEntity.java`.
   - Поля: `Long id`, `PrincipalEntity principal`, `CredentialType type`, `String secretHash`, `String displayValue`, `boolean used`, `Instant createdAt`.
   - Таблица: `credentials`.
   - Репозиторий: `auth/credential/CredentialRepository.java`.
   - Типы (`CredentialType`): `PASSWORD`, `RECOVERY`, `OWNERSHIP`.
   - Значения:
     - `secretHash` — хранение bcrypt-хеша пароля или токена (recovery, ownership).
     - `displayValue` — вспомогательное значение (для ownership — абсолютный путь к файлу; для recovery — сам код для отображения на фронте).
     - `used` — актуально для recovery (одноразовые).
3. Evidence (проверка)
   - Интерфейс: `auth/credential/CredentialVerifier.java` — методы `supports()`, `verify(credential, evidence, context)`, `consumeOnSuccess()`.
   - Реализации (Spring @Component, «CDI-бин-стратегии»):
     - `PasswordCredentialVerifier` — сверяет bcrypt-хеш пароля.
     - `RecoveryCredentialVerifier` — сверяет bcrypt-хеш recovery-кода, при успехе метит used=true.
     - `OwnershipCredentialVerifier` — проверяет наличие файла по пути в `displayValue`.
   - Внедрение: список бинов передаётся в `AuthService`, выбор по `supports()`.

## Бэкенд: генерация и хранение recovery-кодов
1. Генерация в `AuthService.generateRecoveryCodes`:
   - Используется `SecureRandom`.
   - 8 байт, код — Base64 URL без паддинга.
   - Создаётся 5 записей Credential типа `RECOVERY`.
   - `secretHash` = bcrypt(код), `displayValue` = код (для фронтенда).
   - `used=false`, `createdAt` выставляется @PrePersist.
2. Использование:
   - Вход с типом `RECOVERY` ищет все неиспользованные креды, сверяет хеши, при успехе `used=true` сохраняется.

## Бэкенд: право владения файлом (OWNERSHIP Evidence)
1. Генерация в `AuthService.createOwnershipCredential`:
   - Генерируются 32 байта через `SecureRandom`, код — Base64 URL без паддинга.
   - Файл создаётся в каталоге `backend/data/ownership/<login>.txt`.
   - Содержимое файла — только токен (строка).
   - В Credential: `type=OWNERSHIP`, `secretHash`=bcrypt(токен), `displayValue`=абсолютный путь файла, `used=false`.
2. Проверка:
   - Верификатор `OwnershipCredentialVerifier` проверяет существование файла по `displayValue`. Контент не читается; если файл удалён, вход не пройдёт.
   - В `login` передаётся любое значение `value` (в фронте подставляется placeholder), но успех зависит только от наличия файла.
3. Удаление:
   - `AuthService.deleteCredential` при типе `OWNERSHIP` удаляет файл `displayValue` (если существует), затем запись из БД.
4. Риски/поведение:
   - Если файл вручную удалён, вход через ownership невозможен.
   - Путь хранится в БД (displayValue). Секрет остаётся в файле и в bcrypt-хеше; сам токен возвращается клиенту при регистрации для отображения.

## Бэкенд: пароль
1. Credential типа `PASSWORD` хранит bcrypt-хеш.
2. Смена пароля (`/auth/credentials/password`) удаляет старые креды пароля и создаёт новый.
3. Верификатор `PasswordCredentialVerifier` сверяет bcrypt.

## Бэкенд: AuthService (основные функции)
1. `register(RegisterRequest)`:
   - Проверка пустых полей.
   - Проверка уникальности username.
   - Создание Principal.
   - Создание Credential (password).
   - Генерация 5 recovery-кодов.
   - Создание ownership-файла и Credential.
   - Создание сессии (in-memory токен).
   - Возврат `RegisterResponse`: user, token, recoveryCodes, ownershipFilePath, ownershipFileContent.
2. `login(LoginRequest)`:
   - Проверка обязательных полей (для ownership достаточно username+credentialType).
   - Поиск Principal по username.
   - Выбор verifier по CredentialType.
   - Набор Credential для проверки:
     - PASSWORD: все типа PASSWORD.
     - RECOVERY: все типа RECOVERY с used=false.
     - OWNERSHIP: все типа OWNERSHIP.
   - Подготовка evidence:
     - PASSWORD/RECOVERY: строка `value`.
     - OWNERSHIP: если `value` пустой — подставляется placeholder "file-present", verifier проверяет наличие файла.
   - При успехе: для RECOVERY помечает used=true; возвращает LoginResponse с токеном/пользователем.
3. `logout`:
   - Удаляет токен из in-memory map.
4. `findUserByToken`, `findPrincipalByToken`:
   - Парсинг Bearer, поиск в sessions map.
5. `listCredentials(Principal)`:
   - Возврат списка CredentialResponse (id, type, displayValue, used, createdAt).
6. `setPassword`:
   - Удаление старых password-кредов, создание нового с bcrypt.
7. `deleteCredential`:
   - Проверка владельца.
   - Если OWNERSHIP — удаление файла displayValue.
   - Удаление записи.

## Бэкенд: контроллеры и эндпоинты
1. `AuthController` (`/api/auth`):
   - `POST /register` — тело RegisterRequest(username, password), возврат RegisterResponse(user, token, recoveryCodes, ownershipFilePath, ownershipFileContent).
   - `POST /login` — тело LoginRequest(username, credentialType, value), возврат LoginResponse(user, token).
   - `POST /logout` — header Authorization, удаление сессии.
   - `GET /me` — header Authorization, возврат UserDto.
   - `GET /credentials` — список способов пользователя (Authorization обязателен).
   - `POST /credentials/password` — смена/установка пароля (Authorization).
   - `DELETE /credentials/{id}` — удаление способа (Authorization).
   - `POST /credentials/recovery` отсутствует (регенерация отключена).
2. `PointsController` (`/api/points`):
   - `GET` — история точек пользователя, сортировка по timestamp desc.
   - `POST` — отправка точки, расчёт hit, сохранение.

## Бэкенд: сессии
1. In-memory map `sessions: token -> PrincipalEntity`.
2. Токен: UUID (строка).
3. Нет персистентности/refresh/JWT.

## Бэкенд: валидация/безопасность
1. Поля username/password проверяются на пустоту в AuthService; детали диапазонов на фронте (Zod).
2. Hibernate/JPA валидация минимальна (nullable=false, unique=true).
3. Пароли и токены хранятся bcrypt-хешем, recovery-коды одноразовые.
4. OWNERSHIP: проверка только существования файла.
5. CSRF отключён, CORS разрешает localhost:3000.
6. FIDO2/WebAuthn: **не реализовано**. Текущая модель не поддерживает аппаратные токены/подписи; для расширения нужно добавить новый CredentialType, verifier с криптографической проверкой и эндпоинты регистрации/аутентификации ключей.

## Бэкенд: размещение файлов
1. Путь: `backend/data/ownership/<login>.txt`.
2. Директория создаётся при регистрации (mkdirs).
3. Файл содержит строку с Base64 токеном (32 байта).
4. Удаляется при удалении способа OWNERSHIP.

## Фронтенд: обзор
1. CRA структура в `frontend/`.
2. Основные технологии: React 19, Redux Toolkit, React Router DOM 7, Axios, Zod.
3. Стор: `src/app/store.js` — редьюсеры auth, points.
4. Навигация: `Routes` в `App.js`: `/` (Landing), `/app` (Main, защищённый).
5. ProtectedRoute: проверяет наличие токена в Redux.

## Фронтенд: сервисы и API
1. `src/services/apiClient.js` — Axios instance, baseURL env или `http://localhost:8080/api`, авторизация через Bearer из localStorage.
2. `src/services/authApi.js` — методы register, login, logout, me, listCredentials, setPassword, deleteCredential.
3. `src/services/pointsApi.js` — методы fetchResults, submitPoint.

## Фронтенд: Redux slices
1. `authSlice.js`
   - Состояние: user, token, status, error, recoveryCodes, credentials, ownershipFilePath, ownershipFileContent.
   - Thunks: register, login, logout, fetchCurrentUser, listCredentials, deleteCredential.
   - Поведение:
     - register: сохраняет token, user, recoveryCodes, ownershipFilePath, ownershipFileContent в state и token в localStorage.
     - login: сохраняет token, user, чистит error.
     - fetchCurrentUser: обновляет user; при ошибке очищает token и localStorage.
     - logout: очищает user/token/recoveryCodes/credentials/ownershipFile* и localStorage.
     - listCredentials/deleteCredential: обновляют список способов.
2. `pointsSlice.js`
   - Состояние: items, status, error, submissionStatus, currentRadius.
   - Thunks: fetchResults, submitPoint.
   - Поведение: загрузка истории, добавление новой точки в начало списка, установка радиуса.

## Фронтенд: Zod-валидация
1. Файл: `src/validation/schemas.js`.
2. credentialsSchema (регистрация):
   - username: trim, min 1, max 50.
   - password: trim, min 4, max 100.
3. loginSchema:
   - username: min 1.
   - credentialType: enum `password | recovery | ownership`.
   - value: строка до 200 символов; для ownership фронт подставляет placeholder `file-present`.
4. pointSchema:
   - x: число в диапазоне [-4; 4].
   - y: число в (-3; 5), парсинг запятой/точки.
   - r: число из списка [1,2,3,4].
   - Константы ALLOWED_X_VALUES, ALLOWED_R_VALUES, X_RANGE.

## Фронтенд: формы и UI
1. LoginForm (`src/components/LoginForm.jsx`):
   - Режимы: login/register (переключатель).
   - Переключатель способа входа: Пароль, Резервный код, Право владения (кнопка на две колонки).
   - Поля:
     - username (всегда).
     - password (регистрация или login/password).
     - value для recovery (текстовое).
     - ownership: без ввода, только подсказка (убрана по запросу), логин работает по placeholder `file-present`.
   - Ошибки:
     - Валидация Zod, первая ошибка показывается под формой.
     - Ошибка очищается при изменении поля.
   - После регистрации показываются recovery-коды и путь/токен файла права владения.
2. CredentialsManager (`src/components/CredentialsManager.jsx`):
   - Список credential-ов (Пароль, Recovery, Право владения).
   - Показать used статус для recovery.
   - Кнопка «Удалить» — удаляет credential; для OWNERSHIP файл удаляется на бэкенде.
3. PointControls (`src/components/PointControls.jsx`):
   - Радио X (ALLOWED_X_VALUES), ввод Y, радиус R.
   - Валидация Zod pointSchema, ошибки фронта + серверные.
4. AreaChart (`src/components/AreaChart.jsx`):
   - Клик по графику отправляет координаты через pointSchema.
   - Отображает последнюю точку.
5. ResultsTable (`src/components/ResultsTable.jsx`):
   - Ширина на две колонки, placeholder/loader с классом results-table.
6. MainPage (`src/pages/MainPage.jsx`):
   - Grid: PointControls, AreaChart, ResultsTable, CredentialsManager.
7. LandingPage (`src/pages/LandingPage.jsx`):
   - Заголовок + LoginForm.

## Фронтенд: стили
1. LoginForm.css — сегментированные кнопки, ownership кнопка занимает две колонки, стиль ошибок, восстановлен базовый вид.
2. CredentialsManager.css — карточки способов, статусы used/active, отображение кода/типа.
3. MainPage.css — грид 2x, последние элементы (результаты/менеджер) растянуты.
4. Остальные CSS для компонентов (график, таблица, формы).

## Поток регистрации
1. Пользователь вводит username/password, фронт валидирует (credentialsSchema).
2. Запрос `POST /api/auth/register`.
3. Бэкенд:
   - Создаёт Principal, Credential (password).
   - Генерирует 5 recovery-кодов, сохраняет их хеши, выдаёт plaintext в ответ.
   - Создаёт файл `backend/data/ownership/<login>.txt` с 32 байт токеном, сохраняет хеш и путь.
   - Создаёт in-memory сессию (token).
4. Ответ содержит token, user, recoveryCodes, ownershipFilePath, ownershipFileContent (plaintext токен).
5. Фронт:
   - Сохраняет token в Redux/localStorage.
   - Показывает список recovery-кодов и путь/токен файла (однократно).

## Поток логина
1. Пользователь выбирает тип:
   - Пароль: вводит password -> value.
   - Recovery: вводит одноразовый код -> value.
   - Ownership: выбирает тип, value подставляется «file-present».
2. Фронт валидирует (loginSchema).
3. Запрос `POST /api/auth/login` с username, credentialType, value.
4. Бэкенд:
   - Находит Principal по username.
   - Собирает креды нужного типа (учитывает used для recovery).
   - Ownership verifier проверяет наличие файла по displayValue.
   - При успехе создаёт in-memory токен, возвращает user+token.
5. Фронт сохраняет token в Redux/localStorage, переходит на `/app`.

## Поток удаления способа
1. На `/app` в CredentialsManager нажимаем «Удалить» на credential.
2. Запрос `DELETE /api/auth/credentials/{id}`.
3. Бэкенд:
   - Проверяет принадлежность.
   - Если OWNERSHIP — удаляет файл.
   - Удаляет credential из БД.
4. Фронт обновляет список.

## Поток смены пароля
1. Запрос `POST /api/auth/credentials/password` с новым password.
2. Бэкенд удаляет старые PASSWORD креды, создаёт новый с bcrypt.
3. Фронт (при добавлении UI) может вызвать и потом обновить список credentials.

## Points (кратко)
1. DTO:
   - PointRequest(x, y, r).
   - PointResponse(id, x, y, r, hit, timestamp).
2. Hit-логика: в `PointsService.isHit` (треугольник/квадрат/четверть окружности).
3. Привязка к Principal через foreign key principal_id.
4. История сортируется по timestamp desc.

## Каталоги и важные файлы
1. Backend:
   - `src/main/java/ru/vladlenblch/config/SecurityConfig.java`
   - `src/main/java/ru/vladlenblch/auth/AuthService.java`
   - `src/main/java/ru/vladlenblch/auth/AuthController.java`
   - `src/main/java/ru/vladlenblch/auth/credential/*.java`
   - `src/main/java/ru/vladlenblch/auth/principal/*.java`
   - `src/main/java/ru/vladlenblch/auth/dto/*.java`
   - `src/main/java/ru/vladlenblch/points/*.java`
   - `src/main/resources/application.properties`
2. Frontend:
   - `src/validation/schemas.js`
   - `src/components/LoginForm.jsx` + `.css`
   - `src/components/CredentialsManager.jsx` + `.css`
   - `src/components/PointControls.jsx`, `AreaChart.jsx`, `ResultsTable.jsx`
   - `src/features/auth/authSlice.js`, `src/features/points/pointsSlice.js`
   - `src/services/authApi.js`, `apiClient.js`, `pointsApi.js`
   - `src/pages/LandingPage.jsx`, `MainPage.jsx`
   - `src/App.js`, `src/index.js`

## CDI-бин-стратегии (Spring Components)
1. Все CredentialVerifier реализованы как @Component; Spring собирает список и передаёт в AuthService.
2. Добавление нового метода входа = новая реализация, новый CredentialType, сохранение Credential, обновление фронта.
3. Логика выбора стратегии в AuthService: поиск по `supports()` (enum CredentialType).

## Валидация форм и UX на фронтенде
1. LoginForm:
   - Ошибки Zod показываются первой строкой под формой.
   - Ошибка сбрасывается при любом изменении поля.
   - Статус загрузки: кнопка disabled и меняет текст.
2. PointControls:
   - Zod pointSchema, ошибки показываются под формой; серверные ошибки тоже отображаются.
3. ProtectedRoute: без токена редиректит на `/`.
4. Сохранение токена: localStorage key `authToken`.

## Ответы и коды
1. RegisterResponse:
   - user (username)
   - token
   - recoveryCodes (список из 5)
   - ownershipFilePath (абсолютный)
   - ownershipFileContent (plaintext токен 32 байта Base64)
2. LoginResponse:
   - user
   - token
3. CredentialResponse:
   - id, type, displayValue, used, createdAt

## Логика генерации токенов и кодов
1. recovery: 8 байт, Base64 URL без паддинга, bcrypt в БД.
2. ownership: 32 байта, Base64 URL, хранится в файле, bcrypt в БД.
3. session token: UUID (random).

## FIDO2/WebAuthn
1. Не реализовано. Для внедрения потребуется:
   - Новый CredentialType (например, FIDO2).
   - CredentialVerifier, проверяющий подписи/attestation.
   - Эндпоинты для регистрации публичного ключа (challenge/attestation) и логина (assertion).
   - Хранение ключей/криптографических параметров.
2. Текущая версия не вызывает WebAuthn API и не хранит публичные ключи.

## Пример цепочек вызовов
1. Регистрация:
   - AuthController.register -> AuthService.register -> PrincipalRepository.save -> CredentialRepository.save (password) -> generateRecoveryCodes (CredentialRepository.save x5) -> createOwnershipCredential (файл + CredentialRepository.save) -> buildSession -> RegisterResponse.
   - Front: authApi.register -> authSlice.register.fulfilled -> state.user/token/recoveryCodes/ownershipFile* -> LoginForm отображает коды/путь.
2. Логин (пароль):
   - LoginForm validate -> authApi.login -> AuthController.login -> AuthService.login -> CredentialVerifier(PASSWORD) -> buildSession -> token.
   - Front: authSlice.login.fulfilled -> token/user -> navigate /app.
3. Логин (recovery):
   - Аналогично, но выбираются креды type=RECOVERY, consumeOnSuccess=true.
4. Логин (ownership):
   - Front подставляет value='file-present'.
   - AuthService.login выбирает креды type=OWNERSHIP, verifier проверяет `Files.exists(displayValue)`.
5. Удаление ownership:
   - CredentialsManager.delete -> authApi.deleteCredential -> AuthService.deleteCredential (delete file if exists) -> удалить cred.

## Ограничения и риски
1. Сессии in-memory: токены сбрасываются при рестарте.
2. Файл ownership создаётся в файловой системе, путь виден на фронте (plaintext токен тоже выдаётся) — необходимо защищать доступ к файловой системе/каталогу.
3. Нет rate limiting, нет CAPTCHA, нет блокировок по неудачным логинам.
4. Нет HTTPS/сертификатов — требуется на проде.
5. Нет миграций БД; `spring.jpa.hibernate.ddl-auto=update` создаёт таблицы автоматически.
6. Отсутствуют юнит/интеграционные тесты.
7. FIDO2/WebAuthn отсутствуют.

## Что важно помнить
1. Все способы входа независимы: удаление одного не блокирует другие.
2. Recovery коды одноразовые: after use -> used=true.
3. Ownership зависит от наличия файла; если пользователь потерял файл, нужно регистрировать новый аккаунт или добавить новый способ (пароль/recovery).
4. Пароль хранится только в виде bcrypt-хеша.
5. Данные о файле (путь/токен) выдаются только при регистрации.

## Краткое расположение ключевых функций
1. Бэкенд:
   - AuthService.register/login/logout/listCredentials/setPassword/deleteCredential.
   - CredentialVerifier реализации в `auth/credential`.
   - PointsService.isHit — логика попадания в область.
2. Фронтенд:
   - LoginForm — выбор типа входа, отображение recovery и файла.
   - CredentialsManager — управление способами.
   - authSlice — хранит токен, user, recovery, ownership info.
   - schemas.js — Zod схемы.

## Мини-гайд по отладке
1. Проверить наличие ownership файла: `ls backend/data/ownership/`.
2. Проверить, что БД содержит креды: таблица `credentials` (type, display_value, used).
3. Сбросить токены: перезапустить бэкенд (сессии in-memory).
4. Ошибка 401 при login (ownership): убедиться, что файл существует и тип выбран ownership.
5. Ошибка 400 при register: проверить непустые username/password.

## Расширение
1. Добавить FIDO2/WebAuthn: новая стратегия + хранение публичных ключей.
2. Перевести сессии на JWT или persistent refresh tokens.
3. Добавить UI для смены пароля и создания нового ownership файла.
4. Добавить regen recovery (сегодня отключено).
5. Добавить rate limiting и аудит логинов.

## Завершение
Данный документ описывает полную картину текущего состояния проекта: от валидации и UI до моделей БД, генерации кодов и файлов, стратегий проверки, эндпоинтов и потоков. Все изменения касаются отказа от challenge/HMAC, внедрения права владения файлом, сохранения recovery-кодов и адаптации Zod-валидации под новые типы входа. Если требуется углубление или расширение (например, FIDO2/WebAuthn), необходимо добавить новые CredentialType и соответствующие стратегии.

## FIDO2/WebAuthn: теория и план интеграции (пока не реализовано)
### Кратко о протоколе
1. FIDO2/WebAuthn — стандарт аппаратной/программной аутентификации без паролей, основанный на криптографических ключах.
2. Два этапа:
   - Регистрация (attestation): клиент (браузер + аутентификатор) создаёт пару ключей, передаёт публичный ключ серверу вместе с attestation (подпись на challenge), сервер сохраняет ключ и метаданные.
   - Аутентификация (assertion): сервер выдаёт challenge; клиент подписывает его приватным ключом; сервер проверяет подпись публичным ключом, сверяет origin, counter и т.д.
3. Безопасность:
   - Приватный ключ никогда не покидает устройство/аутентификатор.
   - Challenge одноразовый; защита от replay.
   - Валидация origin/RPID привязана к домену.
4. UX: может быть как «passkey» (платформенный), так и «security key» (внешний).

### Что потребуется для интеграции в нашу модель
1. Новый CredentialType (например, `FIDO2`).
2. Сущность/таблица для хранения публичных ключей и метаданных:
   - credentialId (Base64URL), publicKey (COSE/PEM), signCount, attestation type/format (опционально), user handle (пользовательский идентификатор), transports.
   - FK на Principal.
3. Эндпоинты:
   - `POST /api/auth/webauthn/register/options` — выдача challenge и параметров для создания ключа (RP, user, pubKeyCredParams, timeout, authenticatorSelection, attestation).
   - `POST /api/auth/webauthn/register` — приём AttestationObject + clientDataJSON; проверка challenge, origin, RP ID hash, attestation statement; сохранение публичного ключа и signCount.
   - `POST /api/auth/webauthn/login/options` — выдача challenge для входа (assertion) + allowCredentials.
   - `POST /api/auth/webauthn/login` — приём AuthenticatorData + clientDataJSON + signature + userHandle; проверка challenge, origin, RP ID hash, signCount (увеличение), корректность подписи публичным ключом.
4. Верификатор (CredentialVerifier):
   - Реализация `Fido2CredentialVerifier` проверяет подпись assertion, валидирует counter (signCount), сверяет rpIdHash/origin.
   - Для регистрации нужен отдельный сервис для валидации attestation.
5. Сохранение/выбор Credential:
   - При логине с типом FIDO2 ищем по credentialId и principal, проверяем подпись и counter.
   - Если signCount не растёт или подпись неверна — ошибка.
6. Frontend:
   - Использовать WebAuthn API (`navigator.credentials.create` и `navigator.credentials.get`).
   - Потоки:
     - Регистрация: запрос options -> `navigator.credentials.create` -> отправка результата -> сохранение credential на сервере.
     - Логин: запрос options -> `navigator.credentials.get` -> отправка результата -> получение токена.
   - Валидация домена: работать по HTTPS, корректный RP ID.
7. Хранение challenge:
   - Временно на сервере (in-memory или Redis) с привязкой к пользователю/операции, одноразовый.
8. Безопасность/ограничения:
   - Требуется HTTPS.
   - RP ID должен совпадать с доменом.
   - Нужна защита от повторного использования challenge.

### Алгоритмический план в терминах проекта
1. Backend:
   - Добавить `CredentialType.FIDO2`.
   - Создать сущность `FidoCredentialEntity` (credentialId, publicKey, signCount, userHandle, transports, attestationType, createdAt, principal FK).
   - Репозиторий для FIDO2 cred.
   - Сервис для генерации/хранения challenge (можно ConcurrentHashMap + TTL или Redis).
   - Контроллер с четырьмя эндпоинтами (options/register/login).
   - Верификатор `Fido2CredentialVerifier` для assertion (логин).
   - Внедрить в AuthService список verifier-ов, добавить обработку типа `FIDO2`.
2. Frontend:
   - Добавить UI для регистрации FIDO2 (кнопка «Добавить ключ») и логина (кнопка/вкладка «Ключ безопасности/Passkey»).
   - Реализовать вызовы `navigator.credentials.create/get` с данными options/response.
   - Расширить authSlice на новый тип входа.
3. Валидация/данные:
   - Challenge хранить сессией/кешем; после использования удалять.
   - В ответах login/register оставить текущие поля, либо добавить отдельные поля для fido.

### Почему сейчас не реализовано
1. Требует HTTPS и браузерную поддержку WebAuthn (невозможно протестировать без корректного окружения).
2. Добавляет существенную криптографическую валидацию (attestation/assertion) и хранение ключей.
3. Нужна продуманная UX/секьюрность (RP ID, домен, защита от downgrade).

### Как вписать в текущую архитектуру
1. CredentialType расширяется без ломки существующих типов (пароль/recovery/ownership остаются).
2. `CredentialVerifier` список уже используется в AuthService — добавить FIDO2 реализацию.
3. Принцип Principal/Credential/Evidence сохраняется:
   - Principal — тот же.
   - Credential — новая таблица/тип с публичным ключом.
   - Evidence — подпись assertion + проверка counter.
4. Фронтенд — добавить вкладку/кнопку и соответствующие thunks (authApi) и вызовы WebAuthn API.

### Итог
Документ отражает текущую реализацию без FIDO2/WebAuthn. Раздел выше даёт теоретическую базу и план расширения: какие сущности, эндпоинты, проверки и фронтовые шаги нужны, чтобы внедрить FIDO2/WebAuthn в эту модель Principal/Credential/Evidence.
