"""Initialaizer of website"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

#connecting to db


#app creation and configs
def create_app():
    """Creates app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\x8bc\xaa\x9aI\xed\xb8\xe6[Y\x1aF'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:////home/CoFind/V01/instance/{DB_NAME}'
    db.init_app(app)

    #login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #login manager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    #Importing blueprints
    from .views import views
    from .auth import auth

    #database
    from .models import User

    #create database
    create_database(app)

    #registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def create_database(app):
    if not path.exists('src/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created!')
