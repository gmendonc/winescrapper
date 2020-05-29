import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
mongo_db_base_uri = "mongodb+srv://winemaster:winescrape7@projectw-vkqlx.mongodb.net/test?retryWrites=true&w=majority"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@example.com']
    POSTS_PER_PAGE = 3

    MONGO_DB_URI = os.environ.get('MONGO_DB_URI') or mongo_db_base_uri
    MONGO_DATABASE = os.environ.get('MONGO_DATABASE') or 'winedb'
    MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION') or 'wines'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
