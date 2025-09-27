## 🚀 Backend Setup Log: Voluntra Django Project

This log tracks all major installation and configuration changes made to the Django backend, completing Task 1 of the project plan.

### 1. Project Initialization and Dependency Installation

The backend was set up inside a Python virtual environment (`venv`) to isolate dependencies.

| Command | Rationale |
| :--- | :--- |
| `python -m venv venv` | Creates an isolated Python virtual environment. |
| `pip install django djangorestframework psycopg2-binary django-cors-headers python-dotenv` | Installs the full stack of core dependencies: Django, DRF, PostgreSQL driver, CORS handler, and environment variable loader. |
| `django-admin startproject core .` | Initializes the Django project with configuration files in the `core/` directory. |
| `python manage.py startapp api` | Creates the primary application (`api`) to house models, views, and serializers. |

---

### 2. Configuration (`core/settings.py`)

Key changes were made to integrate new libraries and secure the database connection.

| Task | Configuration Change | Rationale |
| :--- | :--- | :--- |
| **App Registration** | Added `'api.apps.ApiConfig'`, `'rest_framework'`, and `'corsheaders'` to `INSTALLED_APPS`. | Enables the API framework, CORS functionality, and the local application logic. |
| **CORS Middleware** | Added `'corsheaders.middleware.CorsMiddleware'` to `MIDDLEWARE`. **(Placed at the top)** | Enables cross-origin sharing, allowing the React frontend (different port/domain) to connect to the backend API. |
| **Allowed Origins** | Set `CORS_ALLOWED_ORIGINS` to `["http://localhost:5173", "http://127.0.0.1:5173"]`. | Explicitly authorizes the Vite development server (default port 5173) to communicate with the API. |
| **Secure Secrets** | Added `from dotenv import load_dotenv; load_dotenv()` and modified `SECRET_KEY` to read from the environment. | **Critical Security Step:** Prevents hardcoding sensitive values (like the database password) and committing them to GitHub. |

---

### 3. Database Setup (PostgreSQL)

A PostgreSQL database named `voluntra_db` was created via pgAdmin 4.

**3.1. `.env` File (Security First)**

A file named `.env` was created and immediately added to `.gitignore`. It contains the following environment variables:

* `SECRET_KEY`
* `DB_NAME`
* `DB_USER`
* `DB_PASSWORD` (The sensitive credential)
* `DB_HOST`
* `DB_PORT`

**3.2. `DATABASES` Configuration (Read from `.env`)**

The `DATABASES` setting was updated to securely read connection details using `os.environ.get()`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}