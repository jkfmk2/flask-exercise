import click
from .extensions import db

def register_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)

@click.command('init-db')
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')

@click.command('reset-db')
def reset_db_command():
    db.drop_all()
    db.create_all()
    click.echo('Reset the database.')