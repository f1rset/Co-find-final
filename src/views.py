"""Non auth routing module"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)



@views.route('/')
def index():
    """
    route to main page of site
    """
    return render_template('index.html')

@views.route('/personal_info')
@login_required
def personal_info():
    return render_template('personal_info.html', user = current_user)

@views.route('/create_activity')
@login_required
def create_activity():
    return render_template('create_activity.html', user = current_user)

@views.route('/home')
@login_required
def home():
    return render_template('home_page.html', user = current_user)

@views.route('/my_activities')
@login_required
def my_activities():
    return render_template('my_activities.html', user = current_user)

@views.route('/my_schedule')
@login_required
def my_schedule():
    return render_template('my_schedule.html', user = current_user)
