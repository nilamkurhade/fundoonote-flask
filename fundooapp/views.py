from flask import jsonify, flash, request
from fundooapp import *
from fundooapp.models import User


@app.route("/login", methods=["GET", "POST"])
def login():
    response = {
        'success': False,
        'message': 'Something bad happened',
        'data': []
    }

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        response['message'] = 'you are logged in now'
        response = jsonify(response)
        login = User.query.filter_by(username=username, password=password).first()
    return response


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
        response['message'] = 'Email address already exists , You can login'
        # flash('Email address already exists , You can login')

        response = jsonify(response)
        # response.status_code = 400

        return response
        # return "Email address already exists , You can login"

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
