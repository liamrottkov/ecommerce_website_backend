import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    # setting up all email config variables
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'liamrottkov@gmail.com'
    MAIL_PASSWORD = 'orydgtdpafeujccx'
    ADMINS = ['liamrottkov@gmail.com']

    STRIPE_SECRET_KEY = 'sk_test_gUH3cKuaDnopSpMj5rATyhOc00kgDm3uWA'
