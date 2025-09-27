@ -1,41 +0,0 @@
1. Installed Django after creating a venv.

>python -m venv 
>pip install django djangorestframework psycopg2-binary django-cors-headers

djangorestframework - For rest apis
psycopg2-binary - For connecting with postgres db
django-cors-headers - For cross origin resource sharing as bot front-end and back-end are running separately.

>django-admin startproject core .
startproject core - creates a new project and keepign the configuration files in the "core" directory. "." Represents to use the currrent directory for the new project.

>python manage.py startapp api
startapp api - This is used to create a new django application. It creates an "api" directory

2. Now once the installation is done, Made changes in core/settings.py file.
2.a.    Added  'api.apps.ApiConfig','rest_framework','corsheaders' in INSTALLED_APPS
2.b.    Added 'corsheaders.middleware.CorsMiddleware' in MIDDLEWARE. NOTE: This should always be in top.
2.c.    To allow the react server, added "http://localhost:5173", "http://127.0.0.1:5173" under CORS_ALLOWED_ORIGINS 

3. Installed postgresql, created a db named voluntra_db. Added the necessary properties for the db in a .env file. these are the properties needed.
SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
Now using the values for these keys in the .env, need to update the DATABASES conf n core/settings.py file
DATABASES = {
    'default': {
        # Reads values from the environment variables (loaded from .env)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
to let the django read .env file, need to install >pip install python-dotenv