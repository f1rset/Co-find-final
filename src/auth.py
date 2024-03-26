"""Auth routes"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, current_user, logout_user
from re import match, compile
#Creating a blueprint
auth = Blueprint('auth', __name__)
DEFAULT_TAGS = {
    'fpn_proj': False,
    'sport_ch': False,
    'additional': False,
    'evening_comp': False,
    'art_proj': False,
    'learn_ch': False,
    'walk': False,
    'volleyball': False,
    'it_meeting': False,
    'it_clubs': False,
    'clubs': False,
    'proj': False,
    'football': False,
    'mafia': False,
    'sport': False,    
}
#Creating routes
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success-log')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            flash('Incorect password, try again!', category='error-log')
        else:
            flash('Username does not exist.', category='error-log')
    return render_template('/login.html')

@auth.route('/logout')
@login_required
def logout():
    """Method to logout"""
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    """Sign Up page"""

    #getting data from form on page
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

    #Checking valid data
        user = User.query.filter_by(username = username).first()
        user_mail = User.query.filter_by(email = email).first()
        matcher = False
        if user:
            flash('Username already exists!', category='error-log')
        elif user_mail:
            flash('This email already in use!', category='error-log')
        elif matcher:
            flash('This is not UCU email!', category='error-log')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error-log')
        elif len(username) < 2:
            flash('Username must be greater than 2 characters.', category='error-log')
        elif password1 != password2:
            flash('Passwowrds don\'t match.')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error-log')
        else:
            #adding user to database
            new_user = User(
                username = username,
                email = email,
                password = generate_password_hash(password1, method='scrypt'),
                reputation = 1000,
                tags = DEFAULT_TAGS
                )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success-log')
            return redirect(url_for('auth.login'))

    return render_template('/signup.html')
