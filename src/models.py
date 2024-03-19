#DO NOT TOUCH THIS CODE
from . import db
from flask_login import UserMixin
from sqlalchemy import func, JSON

#_____________________________________________
#Db for users
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    reputation = db.Column(db.Integer)
    tags = db.Column(JSON)
#___________________________________________
#Db for activities

class Activities(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    creator = db.Column(db.String(150))
    info = db.Column(db.String(1500))
    image = db.Column(db.String(150))
    tags = db.Column(JSON)
    capacity = db.Column(db.Integer)
    checked_users = db.Column(db.String(1500))
    added_users = db.Column(db.String(1500))
