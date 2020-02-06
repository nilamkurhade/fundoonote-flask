from fundooapp import db, ma
import time
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.username, self.email, self.password)

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return password == 'valid'


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()


class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True, nullable=False)
    discription = db.Column(db.String(50))
    color = db.Column(db.String(25))
    is_archive = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)
    is_trash = db.Column(db.Boolean)

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s', '%s')>" % (self.title, self.discription, self.color, self.is_archive,
                                                              self.is_deleted, self.is_trash)


class NotesSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "discription", "color", "is_archive", "is_deleted", "is_trash")


note_schema = NotesSchema()
notes_schema = NotesSchema(many=True)
