# Flask Blog Exercise

This project is an enhanced Flask-based blog application, evolving from the standard Flask tutorial into a modern implementation using SQLAlchemy and popular extensions.

## Project Overview

- **Main Technology:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Database:** SQLite with [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- **Authentication:** [Flask-Login](https://flask-login.readthedocs.io/) and [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
- **Forms:** [Flask-WTF](https://flask-wtf.readthedocs.io/)
- **Admin Interface:** [Flask-Admin](https://flask-admin.readthedocs.io/)
- **Migrations:** [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- **Architecture:** 
    - **Application Factory Pattern:** App initialization in `flaskr/__init__.py`.
    - **Blueprints:** Modular logic for `auth` and `blog`.
    - **Models:** Declarative models in `flaskr/models.py`.
    - **Extensions:** Centralized extension management in `flaskr/extensions.py`.
    - **Forms:** Class-based form definitions in `flaskr/forms.py`.

## Building and Running

### 1. Prerequisites
Ensure you have Python installed. Use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-login flask-bcrypt flask-wtf flask-migrate flask-admin email-validator
```

### 3. Initialize the Database
You can initialize the database using the custom command:
```bash
flask --app flaskr init-db
```
Or use Flask-Migrate for version control:
```bash
flask --app flaskr db upgrade
```

### 4. Create an Admin User
To access the admin interface (`/admin`), create a user with admin privileges:
```bash
flask --app flaskr create-admin
```

### 5. Run the Application
```bash
flask --app flaskr run --debug
```
The application will be available at `http://127.0.0.1:5000`.

## Development Conventions

- **Models:** Define all database schemas in `flaskr/models.py`.
- **Forms:** Use `flaskr/forms.py` for all input validation.
- **Security:** 
    - Use `current_user` from Flask-Login for session management.
    - Use `@login_required` to protect views.
    - Password hashing is handled automatically by the `User.password` setter using Bcrypt.
- **Admin:** New models should be registered in `flaskr/admin.py`.

## Key Files

- `flaskr/extensions.py`: Initialization of SQLAlchemy, LoginManager, etc.
- `flaskr/models.py`: Database models (User, Post).
- `flaskr/auth.py`: Authentication views.
- `flaskr/blog.py`: Blog CRUD views.
- `flaskr/forms.py`: WTForms definitions.
- `flaskr/admin.py`: Flask-Admin configuration.
- `flaskr/commands.py`: Custom CLI commands.
