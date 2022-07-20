from sqlalchemy.sql import func
from . import db
from flask_login import UserMixin


class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    pic =db.Column(db.String(),nullable=True)
    datee = db.Column(db.DateTime(timezone = True),default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    notes = db.relationship('Note')
    