import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user

from .models import User
from .forms import LoginForm, RegistrationForm
from .extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        
        if error is None:
            try:
                user = User(username=username)   
                user.password = password
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)
        
    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not user.check_password(password):
            error = "Incorrect password."
        
        if error is None:
            login_user(user)
            return redirect(url_for("blog.index"))
        
        flash(error)
        
    return render_template("auth/login.html", form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("blog.index"))