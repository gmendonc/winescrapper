from pymongo import MongoClient

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_winedb():
    if 'winedb' not in g:
        g.winedb = MongoClient(current_app.config['MONGO_DB_URI'])
   
    return g.winedb
        
def close_winedb(e=None):
    db = g.pop('winedb', None)

    if db is not None:
        db.close()

def init_winedb():
    print("Estou no init_winedb")
    db = get_winedb()

@click.command('init-winedb')
@with_appcontext
def init_winedb_command():
    print("Estou no init_winedb_command")
    init_winedb()
    click.echo('Initialized the Mongo database.')

def init_app(app):
    print("Estou no init_app")
    app.teardown_appcontext(close_winedb)
    app.cli.add_command(init_winedb_command)
