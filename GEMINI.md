# Flask Blog Exercise

This project is a Flask-based blog application, following the standard Flask tutorial architecture. It provides a foundational implementation of a web application with user authentication and blog post management.

## Project Overview

- **Main Technology:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Database:** SQLite
- **Architecture:** 
    - **Application Factory Pattern:** The app is initialized in `flaskr/__init__.py`.
    - **Blueprints:** Modularized logic for authentication (`flaskr/auth.py`) and blog functionality (`flaskr/blog.py`).
    - **Database Management:** Handled in `flaskr/db.py` with schema defined in `flaskr/schema.sql`.
    - **Templates:** Uses Jinja2 for rendering HTML, located in `flaskr/templates`.
    - **Static Assets:** CSS and other assets are in `flaskr/static`.

## Building and Running

### 1. Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment.

### 2. Install Dependencies
While a `requirements.txt` is not present, the core dependencies are:
- `flask`
- `werkzeug`

```bash
pip install flask
```

### 3. Initialize the Database
Before running the app for the first time, or to reset it, run:
```bash
flask --app flaskr init-db
```

### 4. Run the Application
Start the development server:
```bash
flask --app flaskr run --debug
```
The application will be available at `http://127.0.0.1:5000`.

### 5. Production Entry Point
`wsgi.py` is provided as an entry point for WSGI servers (like Gunicorn or uWSGI).

## Development Conventions

- **Factory Pattern:** Always use `flaskr.create_app()` to instantiate the application.
- **Instance Folder:** Local configuration (like the SQLite DB) is stored in the `instance/` directory, which is excluded from version control.
- **Authentication:** Use the `@login_required` decorator from `flaskr.auth` to protect views.
- **Database Access:** Use `flaskr.db.get_db()` within an application context to get a database connection.
- **URL Rules:** The `blog.index` endpoint is mapped to the root URL (`/`).

## Key Files

- `flaskr/__init__.py`: App factory and blueprint registration.
- `flaskr/auth.py`: User registration, login, and session management.
- `flaskr/blog.py`: CRUD operations for blog posts.
- `flaskr/db.py`: SQLite connection and CLI command definitions.
- `flaskr/schema.sql`: SQL definitions for `user` and `post` tables.
- `wsgi.py`: WSGI entry point.
