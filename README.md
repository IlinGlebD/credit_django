# Студент: Ильин Г.Д., Сорокун С.Р., ФБИ-32

# Курсовая работа на тему "Разработка ИАД-системы для анализа кредитоспособности клиентов банка"

## Как запустить проект

1. **Клонировать репозиторий и перейти в папку:**
   ```bash
   git clone <repo_url>
   cd credit_django
2. **Создать виртуальное окружение и активировать:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
3. **Установить зависимости:**
    ```bash
    pip install -r requirements.txt
4. **Сделать миграции:**
    ```bash
    python manage.py migrate
5. **Запустить сервер:**
    ```bash
    python manage.py runserver
6. **Открыть в браузере:**
    ```bash
    http://127.0.0.1:8000/