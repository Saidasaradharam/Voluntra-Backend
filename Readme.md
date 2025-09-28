# Voluntra-Website Backend (Django REST Framework)  
## NGO Management Platform API  

##  Tech Stack  

| Category       | Technology                  | Notes                                                       |  
|----------------|-----------------------------|-------------------------------------------------------------|  
| Framework      | Django                      | Robust Python web framework for backend logic.              |  
| API Layer      | Django REST Framework (DRF) | Provides RESTful APIs for the client (frontend).            |  
| Database       | SQLite (dev) / PostgreSQL   | Default dev DB is SQLite, but production-ready with Postgres. |  
| Auth Flow      | JWT (SimpleJWT)             | Secure authentication with role-based access control.       |  
| Storage        | Django ORM                  | Used for persistence of users, events, applications, etc.   |  

---

## Key Features & Architecture  

- **Decoupled Architecture** → Exposes APIs consumed by the React/Vite frontend.  
- **Custom User Model** → Supports `Volunteer`, `NGO`, and `Corporate` roles.  
- **Role-Based Permissions** → Ensures each role only accesses their allowed endpoints.  
- **Events & Applications** → NGOs can create/manage events, volunteers can apply.  
- **Donations Module** → Corporates can donate to NGOs, with full transaction tracking.  
- **Certificates** → Volunteers can download event participation certificates.  

---

## ⚙️ Local Setup Guide  

### Clone the Repository  
```bash
git clone https://github.com/Saidasaradharam/Voluntra-Backend.git
cd Voluntra-Backend
```

Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
Install Dependencies
`pip install -r requirements.txt`

Run Migrations
`python manage.py migrate`

Create Superuser
`python manage.py createsuperuser`

Start the Development Server
`python manage.py runserver`


Backend runs on http://127.0.0.1:8000/


