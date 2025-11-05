import json, os, flask, tempfile
from flask import session

from handlers import copy
from db import posts, users, helpers

blueprint = flask.Blueprint("login", __name__)

@blueprint.route('/loginscreen')
def loginscreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()

    # First check if already logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title,
            subtitle=copy.subtitle)

@blueprint.route('/login', methods=['POST'])
def login():
    """Log in the user.

    Using the username and password fields on the form, create, delete, or
    log in a user, based on what button they click.
    """
    db = helpers.load_db()

    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    resp.set_cookie('username', username)
    resp.set_cookie('password', password)

    submit = flask.request.form.get('type')
    if submit == 'Sign Up':
        # store temporarily in the session
        session['temp_username'] = username
        session['temp_password'] = password
        
        if users.new_user(db, username, password) is None and username and password:
            flask.flash(f'Username {username} already taken!', 'danger')
            return flask.redirect(flask.url_for('login.Loginscreen'))

        flask.flash(f'User {username} created successfully!', 'success')
        return flask.redirect(flask.url_for('login.signup'))
    elif submit == 'Delete':
        if users.delete_user(db, username, password):
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('User {} deleted successfully!'.format(username), 'success')

    return resp

@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/signup')
def signup():
    question_list = [
        # Light & Fun
        "My most controversial food opinion",
        "The most spontaneous thing I’ve ever done",
        "The fictional world I want to live in",
        "My go-to comfort movie or show",
        "If we started a band, its name would be",
        "What I would do if I won the lottery tomorrow",
        
        # Personality & Preferences
        "Something small that instantly makes my day better",
        "My love language is",
        "I'm currently obsessed with",
        "One hobby I've always wanted to try",
        
        # Deep & Emotional
        "One lesson I've learned the hardway",
        "My idea of a perfect relationship is",
        "What I most value in a partner is",
        "I feel most alive when",
        "The last time I felt truley at peace was",
        
        # Flirty / Romantic
        "My ideal first date is",
        "The quality I find most attractive is",
        "We're made for each other if",
        
        # Random & Thought-provoking
        "If I could re-live one day of my life, it would be",
        "If I could have dinner with any 3 people, I would choose",
        "If my life were a movie, my theme song would be",
        "Something I can talk about for hours",
        "If time and money didn’t matter, I would",
    ]

    interest_list = [
        "Biking", "Basketball", "Fishing", "Soccer", "Pickleball",
        "Gaming", "Ninteno", "Skyrim", "Minecraft", "Movies", "Marvel", "Lord of the Rings",
        "Coding", "Art", "Music", "Piano", "Jazz", 
        "Widdling", "Sewing", "Cooking"
    ]

    return flask.render_template('signup.html', question_list=question_list, interest_list=interest_list)

@blueprint.route('/finish_signup', methods=['POST'])
def finishSignup():
    db = helpers.load_db()

    # Retrieve the username and password from session
    username = session.get('temp_username')
    password = session.get('temp_password')

    if not username or not password:
        flask.flash("Missing login info, please try again.", "danger")
        return flask.redirect(flask.url_for('login.index'))
    
    # Get all form values (from POST)
    firstName = flask.request.form.get('fname')
    age = flask.request.form.get('age', type=int)
    minAge = flask.request.form.get('minAge', type=int)
    maxAge = flask.request.form.get('maxAge', type=int)
    gender = flask.request.form.get('gender')

    interests = flask.request.form.getlist('interests')  # <-- list of strings

    quest1 = flask.request.form.get('question1')
    answer1 = flask.request.form.get('answer1')
    quest2 = flask.request.form.get('question2')
    answer2 = flask.request.form.get('answer2')
    quest3 = flask.request.form.get('question3')
    answer3 = flask.request.form.get('answer3')

    # Python data (to be sent to JSON file)
    userData = {
        "name": firstName,
        "age": age,
        "ageRange": [minAge, maxAge],
        "gender": gender,
        "interests": interests,  
        "question1": quest1,
        "answer1": answer1,
        "question2": quest2,
        "answer2": answer2,
        "question3": quest3,
        "answer3": answer3
    }

    users.create_user_data(db, userData, username)

    # Continue your logic (redirect, database insert, etc.)
    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    resp.set_cookie('username', username)
    resp.set_cookie('password', password)

    session.pop('temp_username', None)
    session.pop('temp_password', None)

    return resp

@blueprint.route('/matches')
def matches():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('matches.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts)

@blueprint.route('/account')
def account():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # get the info for the user's feed
    data = users.get_user_data(db, user)
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('account.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, data=data)

@blueprint.route('/')
def index():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('feed.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts)
