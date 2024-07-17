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
