"""Non auth routing module"""
from . import db
from .models import User
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)
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


@views.route('/')
def index():
    """
    route to main page of site
    """
    return render_template('index.html')

@views.route('/personal_info', methods = ['GET', 'POST'])
@login_required
def personal_info():

    if request.method == 'POST':
        # form_id = request.form['form_id']
        user = current_user
        try:
            if request.form['old_password']:
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                if check_password_hash(user.password, old_password):
                    user.password = generate_password_hash(new_password)
                    db.session.commit()
                    flash('Your password has been changed', category = 'success')
                else:
                    flash('Old password does not match!', category = 'error')

        except KeyError:
            #adding tags
            tags_store = DEFAULT_TAGS
            for i in tags_store:
                if request.form.get(i):
                    tags_store[i] = True
                else:
                    tags_store[i] = False
            user.tags = tags_store
            db.session.commit()
            flash('Your tags have been refreshed!', category='success')

    return render_template('personal_info.html', user = current_user)

@views.route('/create_activity')
@login_required
def create_activity():
    if request.method == 'POST':
        pass
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
