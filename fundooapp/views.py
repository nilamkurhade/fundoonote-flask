from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from flask import jsonify, flash, request, render_template, url_for, session, redirect
from flask_login import current_user
from werkzeug.security import *
from fundooapp import *
from fundooapp.models import User, Notes, notes_schema, note_schema, db, User
from werkzeug.utils import secure_filename
import os
# from fundooapp.oauth2 import authorization, require_oauth
import time

app.config["IMAGE_UPLOADS"] = "/home/admin1/PycharmProjects/flask/fundoonote_flask/fundooapp/image"
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
def login_form():
    return render_template('login.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    response = {
        'success': False,
        'message': 'Something bad happened',
        'data': []
    }

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        response['message'] = 'you are logged in now'
        response = jsonify(response)
        # return redirect(url_for('login'))
        login = User.query.filter_by(email=email, password=password).first()
        print(login)
    return response


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
        return redirect(url_for('login'))

    else:
        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    response['success'] = True
    response['message'] = 'registration successful '

    response = jsonify(response)

    response.status_code = 200
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    del session['id']
    return redirect('/home')


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
        note = Notes.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204


api.add_resource(NotesResource, '/notes/<int:note_id>')


class NoteCollaborator(Resource):

    def put(self, note_id):
        notes = Notes.query.get_or_404(note_id)
        user_id = request.json['collaborate']
        print("userrrrrrr", user_id)
        user = User.query.get(user_id)
        notes.collaborator.append(user)
        db.session.commit()
        return "note collaborated"


api.add_resource(NoteCollaborator, '/notes/collaborator/<int:note_id>')


# @app.route('/home', methods=('GET', 'POST'))
# def home():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             user = User(username=username)
#             db.session.add(user)
#             db.session.commit()
#         session['id'] = user.id
#         return redirect('/')
#     user = current_user()
#     if user:
#         clients = OAuth2Client.query.filter_by(user_id=user.id).all()
#     else:
#         clients = []
#     return render_template('home.html', user=user, clients=clients)
#
#
# @app.route('/create_client', methods=('GET', 'POST'))
# def create_client(username=None):
#     user = current_user()
#     if not user:
#         return redirect('/')
#     if request.method == 'GET':
#         return render_template('create_client.html')
#
#     client_id = gen_salt(24)
#     client_id_issued_at = int(time.time())
#     client = OAuth2Client(
#         client_id=client_id,
#         client_id_issued_at=client_id_issued_at,
#         user_id=user.id,
#     )
#
#     if client.token_endpoint_auth_method == 'none':
#         client.client_secret = ''
#     else:
#         client.client_secret = gen_salt(48)
#
#     form = request.form
#     client_metadata = {
#         "client_name": form["client_name"],
#         "client_uri": form["client_uri"],
#         "grant_types": split_by_crlf(form["grant_type"]),
#         "redirect_uris": split_by_crlf(form["redirect_uri"]),
#         "response_types": split_by_crlf(form["response_type"]),
#         "scope": form["scope"],
#         "token_endpoint_auth_method": form["token_endpoint_auth_method"]
#     }
#     client.set_client_metadata(client_metadata)
#     db.session.add(client)
#     db.session.commit()
#     return redirect('/home')
#
#
# @app.route('/oauth/authorize', methods=['GET', 'POST'])
# def authorize():
#     user = current_user()
#     if request.method == 'GET':
#         try:
#             grant = authorization.validate_consent_request(end_user=user)
#         except OAuth2Error as error:
#             return error.error
#         return render_template('authorize.html', user=user, grant=grant)
#     if not user and 'username' in request.form:
#         username = request.form.get('username')
#         user = User.query.filter_by(username=username).first()
#     if request.form['confirm']:
#         grant_user = user
#     else:
#         grant_user = None
#     return authorization.create_authorization_response(grant_user=grant_user)
#
#
# @app.route('/oauth/token', methods=['POST'])
# def issue_token():
#     return authorization.create_token_response()
#
#
# @app.route('/oauth/revoke', methods=['POST'])
# def revoke_token():
#     return authorization.create_endpoint_response('revocation')
#
#
# @app.route('/api/me')
# @require_oauth('profile')
# def api_me():
#     user = current_token.user
#     return jsonify(id=user.id, username=user.username)
