from flask import jsonify, flash, request, render_template, url_for
from flask_login import login_required, logout_user
from fundooapp import *
from fundooapp.models import User, Notes, notes_schema, note_schema
from flask import request, redirect
from werkzeug.utils import secure_filename
import os
from flask import request  # change


app.config["IMAGE_UPLOADS"] = "/home/admin1/PycharmProjects/fundoonote_flask/fundooapp/image"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                print("Image saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("uploadfile.html")


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
    return redirect(url_for('login'))


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


class NotesListResource(Resource):
    def get(self):
        posts = Notes.query.all()
        return notes_schema.dump(posts)

    # new
    def post(self):
        new_note = Notes(
            title=request.json['title'],
            discription=request.json['discription'],
            color=request.json['color'],
            is_archive=request.json['is_archive'],
            is_deleted=request.json['is_deleted'],
            is_trash=request.json['is_trash']
        )
        db.session.add(new_note)
        db.session.commit()
        return note_schema.dump(new_note)


api.add_resource(NotesListResource, '/notes')


class NotesResource(Resource):
    def get(self, note_id):
        note = Notes.query.get_or_404(note_id)
        return note_schema.dump(note)

    def patch(self, note_id):
        note = Notes.query.get_or_404(note_id)

        if 'title' in request.json:
            note.title = request.json['title']
        if 'discription' in request.json:
            note.discription = request.json['content']
        if 'color' in request.json:
            note.color = request.json['content']
        if 'is_archive' in request.json:
            note.is_archive = request.json['content']
        if 'is_deleted' in request.json:
            note.is_deleted = request.json['content']
        if 'is_trash' in request.json:
            note.is_trash = request.json['content']

        db.session.commit()
        return note_schema.dump(note)

    def delete(self, note_id):
        post = Notes.query.get_or_404(note_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(NotesResource, '/notes/<int:note_id>')
