from flask import jsonify, flash, request, render_template, url_for
from flask_login import login_required, logout_user
from werkzeug.utils import redirect
from fundooapp import *
from fundooapp.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile', methods=["GET"])
def profile():
    return render_template('profile.html')


@app.route('/login')
def login():
    return render_template('login.html')


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     response = {
#         'success': False,
#         'message': 'Something bad happened',
#         'data': []
#     }
#
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#
#         # response['message'] = 'you are logged in now'
#         # response = jsonify(response)
#         return redirect(url_for('login'))
#         login = User.query.filter_by(username=username, password=password).first()
#     return response


@app.route('/signup')
def signup_form():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():

    response = {
        'success': False,
        'message': 'Something bad happened',
        'data': []
    }

    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in database

    if user:
        flash('Email address already exists , You can login')
        return redirect(url_for('signup'))

    else:
        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, username=username, password=password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    response['success'] = True
    response['message'] = 'registration successful '

    response = jsonify(response)

    response.status_code = 200
    return response


@app.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('login'))
