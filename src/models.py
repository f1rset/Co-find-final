#DO NOT TOUCH THIS CODE
from . import db
from flask_login import UserMixin
from sqlalchemy import func


#_____________________________________________
#Db for users
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    # tags = db.Column(db.String(800))

#___________________________________________
#Db for activities

class Activities(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    creator = db.Column(db.String(150))
    name = db.Column(db.String(200))
    info = db.Column(db.String(1500))
    image = db.Column(db.String(150))
    tags = db.Column(db.String(800))
    capacity = db.Column(db.Integer)
    checked_users = db.Column(db.String(1500))
    added_users = db.Column(db.String(1500))
