## Backend Setup Log: Voluntra Django Project

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
```

---
---
## Backend Development Log: Database Schema & API Layer

This log documents the successful completion of **Task 2: Dashboard Functionality**, which involved defining the entire application schema and creating the REST API endpoints using Django REST Framework (DRF).

### 1. Model Implementation (Task 2, Part 1)

| Task | Detail | Rationale/Outcome |
| :--- | :--- | :--- |
| **Model Definition** | Defined four core models in `api/models.py`: `CustomUser`, `Event`, `VolunteerApplication`, and `CorporateDonations`. | Establishes the entire database schema required by the application, including core relational logic. |
| **CustomUser** | Extended `AbstractUser` and added the `role` field with `NGO`, `Volunteer`, and `Corporate` choices. | Enables secure role-based access control and dynamic dashboard routing across the application. |
| **Enrollment Logic** | Created `VolunteerApplication` with `unique_together = ('event', 'volunteer')` and a status field. | Ensures a Volunteer can only apply to an event once and allows the NGO to track the application status. |
| **Settings** | Added `AUTH_USER_MODEL = 'api.CustomUser'` to `core/settings.py`. | Instructed Django to use the custom model for authentication, a necessary prerequisite for all system features. |

#### Verification

* **Database:** PostgreSQL database tables were successfully created via `python manage.py migrate`.

---

### 2. API Endpoints (Task 2, Part 2)

| File | Change | Rationale/Outcome |
| :--- | :--- | :--- |
| **`api/serializers.py`** | Defined four serializers (`UserSerializer`, `EventSerializer`, etc.) using `read_only_fields` extensively. | Converts complex model data into JSON for the frontend, ensuring sensitive system-managed fields (`donor`, `created_by`, `transaction_id`, etc.) are protected. |
| **`api/views.py`** | Created four `ModelViewSet`s with custom permission and queryset methods (`get_permissions`, `get_queryset`). | Implements all necessary CRUD operations and enforces robust **Role-Based Access Control (RBAC)**. |
| | **RBAC & Filtering** | Logic restricts `CREATE/UPDATE/DELETE` for **Events** to NGOs only, and ensures users only retrieve data relevant to their role (e.g., volunteers only see their applications). |
| **`api/urls.py`** | Configured `DefaultRouter` to register ViewSets for `profile/`, `events/`, `applications/`, and `donations/`. | Generates clean, RESTful URLs (e.g., `GET /api/events/`) automatically, making the API accessible to the React frontend. |

---
