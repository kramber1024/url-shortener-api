# URL Shortener API

<a href="https://github.com/kramber1024/url-shortener-api/actions/workflows/tests.yml" target="_blank"><img src="https://github.com/kramber1024/url-shortener-api/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
<a href="https://app.codecov.io/github/kramber1024/url-shortener-api/tree/main" target="_blank"><img src="https://img.shields.io/codecov/c/github/kramber1024/url-shortener-api" alt="Coverage">
</a>

## Stack & Features

- 🌐 [**FastAPI**](https://fastapi.tiangolo.com/) for Python backend.
    - 📋 [Pydantic](https://docs.pydantic.dev/), used for data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org/) as SQL Database.
- 🐋 [**Docker**](https://www.docker.com/) for development, testing and production.
- 🏭 CI/CD with [**GitHub Actions**](https://github.com/kramber1024/url-shortener-api/actions/).
- 🔑 [**JWT**](https://jwt.io/) based authentication.
- ✅ Tests with [**Pytest**](https://pytest.org/).
- 🔒 Secure password hashing.
- ✉️ Password recovery with email.

> [!WARNING]
> This repository is part of a larger project that consists of multiple repositories. Using this repository on its own is not recommended, as it may not function correctly without the other components of the project. For complete functionality and proper integration, please refer to the [kramber1024/url-shortener](https://github.com/kramber1024/url-shortener).

## Local launch

### Requirements

- 🐍 [**Python 3.12**](https://www.python.org/)

### Installation

Clone the repository:
```bash
git clone https://github.com/kramber1024/url-shortener-api.git
```

Navigate to the project directory:
```bash
cd url-shortener-api
```

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- On Linux and macOS:

    ```bash
    source venv/bin/activate
    ```
- On Windows:

    ```bat
    .\venv\Scripts\activate
    ```

Install [**Poetry**](https://python-poetry.org/) package manager:
```bash
pip install poetry
```

Install dependencies required to run the project:
```bash
poetry install --only main --no-root
```

Run the project:
```bash
python -m app.main
```

You can see the result by navigating to one of the following addresses:
- **http://127.0.0.1:26801/api/docs** - Swagger UI
- **http://127.0.0.1:26801/api/redoc** - ReDoc

> [!NOTE]
> Documentation for testing, running in Docker, and environment variables can be found in [**DEVELOPMENT.md**](./DEVELOPMENT.md)

## License

This project is licensed under the terms of the [**MIT license**](./LICENSE).
