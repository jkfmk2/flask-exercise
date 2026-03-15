import os
from flask import Flask
from .extensions import db, login_manager, migrate
from .models import User

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    os.makedirs(app.instance_path, exist_ok=True)


    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from .commands import register_commands
    register_commands(app)

    from . import auth
    from . import blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app