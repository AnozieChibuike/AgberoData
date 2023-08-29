from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    otp = db.Column(db.Integer)
    fullname = db.Column(db.String(90))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
@login.user_loader
def load_user(id):
    return User.query.get(int(id))