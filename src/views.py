"""Non auth routing module"""
from . import db
from .models import User, Activities
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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

@views.route('/create_activity', methods = ['GET', 'POST'])
@login_required
def create_activity():
    if request.method == 'POST':
        name = request.form.get('act-name')
        creator = current_user.username
        info = request.form.get('description')
        image = request.form.get('image')
        deadline_str = request.form['deadline']
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid deadline format. \
Please enter in the format YYYY-MM-DDTHH:MM.', category="act-error")

        if deadline <= datetime.now():
            flash('Deadline must be in the future.', category="act-error")

        tags = DEFAULT_TAGS
        for i in tags:
            if request.form.get(i):
                tags[i] = True
            else:
                tags[i] = False

        capacity = int(request.form.get('capacity'))
        comments = request.form.get('comments')== 'on'
        users = {}

        if len(name)<2:
            flash('The activity name is too short!', category='act-error')
        elif len(info)<5:
            flash('The activity information is too short!', category='act-error')
        elif capacity <= 0:
            flash('The capacity is too low!', category='act-error')
        else:
            new_activity = Activities(
                name = name,
                creator = creator,
                info = info,
                deadline = deadline,
                image = image,
                tags = tags,
                capacity = capacity,
                comments = comments,
                users = users
            )
            db.session.add(new_activity)
            db.session.commit()
            flash('Activity created', category='act-success')

    return render_template('create_activity.html', user = current_user)

@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        act_id = int(request.form['join'])

        activity = Activities.query.filter_by(id = act_id).first()
        users = activity.users.copy()
        users[current_user.username] = False
        activity.users = users
        db.session.commit()

    result_activities = []
    for i in Activities.query.all():
        for key, value in current_user.tags.items():
            if i.tags[key] is True and value is True and i.creator != current_user.username \
                and current_user.username not in i.users.keys() and i.deadline > datetime.now():
                result_activities.append(i)
                break

    return render_template('home_page.html', user = current_user,
                           result_activities=result_activities)

@views.route('/my_activities')
@login_required
def my_activities():
    return render_template('my_activities.html', user = current_user)

@views.route('/my_schedule', methods = ['GET', 'POST'])
@login_required
def my_schedule():

    if request.method == 'POST':
        act_id = int(request.form['leave'])
        activity = Activities.query.filter_by(id = act_id).first()
        users = activity.users.copy()
        if activity.deadline <= datetime.now():
            flash('You cannot leave activity after deadline!', category='schedule-error')
        else:
            users.pop(current_user.username)
            activity.users = users
            db.session.commit()

    result_activities = []
    for i in Activities.query.all():
        if current_user.username in i.users.keys():
            result_activities.append(i)
    return render_template('my_schedule.html', user = current_user,
                           result_activities = result_activities)
