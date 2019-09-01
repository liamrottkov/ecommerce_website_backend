from app import app, db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    quantity = db.Column(db.Integer)

class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    message = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default=datetime.now().date())

class Checkout(db.Model):
    checkout_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Integer)

    # create methods for setting and getting password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    # create a method for generating a token and verifying that token
    def get_token(self, expires_in=86400):
        return jwt.encode(
            { 'user_id' : self.id, 'exp' : time() + expires_in },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')


    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithm=['HS256']
            )['user_id']
        except:
            return


        return User.query.get(id)
