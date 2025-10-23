# Social Media (Django)

Lightweight Django-based social media project with a single `core` app. This README covers setup, configuration, and common tasks.

## Features
- Basic user authentication (signin, logout)
- Post feed and user posts
- Static and media file handling
- MySQL backend (configurable)

## Requirements
- Python 3.8+
- pip
- virtualenv (recommended)
- MySQL server and client libraries

## Quick setup

1. Clone repository
   - git clone <repo-url>
   - cd <repo>

2. Create and activate virtual environment
   - python -m venv .venv
   - source .venv/bin/activate  (macOS/Linux)
   - .venv\Scripts\activate     (Windows)

3. Install dependencies
   - pip install -r requirements.txt
   - If requirements.txt is missing, at minimum install:
     - pip install django mysqlclient python-dotenv

4. Configure environment
   - Do NOT commit secrets. Create a `.env` or set environment variables:
     - SECRET_KEY
     - DEBUG (0 or 1)
     - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
   - Recommended: use django-environ or python-dotenv to load env vars and avoid hardcoding secrets in settings.

5. Database
   - Create a MySQL database and grant a user access.
   - Update settings or environment variables with DB credentials.

6. Migrate and create superuser
   - python manage.py migrate
   - python manage.py createsuperuser

7. Collect static (production)
   - python manage.py collectstatic

8. Run development server
   - python manage.py runserver

## Project layout (relevant)
- social_media/ (Django project)
  - settings.py         (project settings; replace hardcoded secrets with env vars)
  - urls.py
  - wsgi.py
- core/                 (main app)
- templates/
- static/
- media/                (user uploaded files)

## Notes
- Current settings.py uses MySQL and includes LOGIN_URL = 'signin', LOGIN_REDIRECT_URL = 'post_feed', LOGOUT_REDIRECT_URL = 'signin'.
- Switch DEBUG to False in production and configure ALLOWED_HOSTS.
- Secure SECRET_KEY and DB credentials using environment variables or a secrets manager.

## Contributing
- Fork, create a feature branch, add tests, and open a pull request.

## License
- Add your project license file (e.g., MIT) as appropriate.