import click
from flask.cli import with_appcontext
from getpass import getpass
from .extensions import db
from .models import User

def register_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)
    app.cli.add_command(create_admin_command)

@click.command('init-db')
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')

@click.command('reset-db')
def reset_db_command():
    db.drop_all()
    db.create_all()
    click.echo('Reset the database.')

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    username = input('Username: ')
    if User.query.filter_by(username=username).first():
        click.echo('User already exists')
        return
    password = getpass('Password: ')
    confirm = getpass('Confirm Password: ')

    if password != confirm:
        click.echo('Password mismatch')
        return
    
    user = User(username=username, is_admin=True)
    user.password = password

    db.session.add(user)
    db.session.commit()

    click.echo('Admin created successfully')
