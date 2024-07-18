# URL Shortener API

<a href="https://github.com/kramber1024/url-shortener-api/actions/workflows/tests.yml" target="_blank"><img src="https://github.com/kramber1024/url-shortener-api/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
<a href="https://app.codecov.io/github/kramber1024/url-shortener-api/tree/main" target="_blank"><img src="https://img.shields.io/codecov/c/github/kramber1024/url-shortener-api" alt="Coverage">
</a>

## Технологический стек и фичи

- 🌐 [**FastAPI**](https://fastapi.tiangolo.com/) для апи сервиса.
    - 📋 [Pydantic](https://docs.pydantic.dev/), используется Fastapi для валидации данных и управления настройками.
    - 💾 [PostgreSQL](https://www.postgresql.org/) для хранения данных.
- 🐋 [**Docker**](https://www.docker.com/) для разработки, тестирования и деплоя.
- 🔑 [**JWT**](https://jwt.io/) для авторизации пользователей.
- ✅ Тестирование с помощью [**Pytest**](https://pytest.org/).
- 🔒 Надёжное хеширование паролей.
- ✉️ Восстановление паролей через почту.

## Локальный запуск

### Требования

- 🐍 [**Python 3.12.x**](https://www.python.org/)

### Запуск

Клонируем репозиторий
```bash
git clone https://github.com/kramber1024/url-shortener-api.git
```

Переходим в папку с проектом
```bash
cd url-shortener-api
```

Создаём виртуальное окружение
```bash
python -m venv venv
```

Активируем виртуальное окружение
- На Windows

    ```bat
    .\venv\Scripts\activate
    ```
- На Linux и macOS

    ```bash
    source venv/bin/activate
    ```

Устанавливаем Poetry
```bash
pip install poetry
```

Устанавливаем зависимости, необходимые для запуска проекта
```bash
poetry install --only main --no-root
```

Запускаем проект
```bash
python -m app.main
```

Увидеть результат можно, перейдя по одному из адресов:
- **http://127.0.0.1:26801/api/docs** - Swagger UI
- **http://127.0.0.1:26801/api/redoc** - ReDoc

**Документацию по тестированию, запуску в докере и переменным окружения можно найти в [DEVELOPMENT.md](./DEVELOPMENT.md)**.
