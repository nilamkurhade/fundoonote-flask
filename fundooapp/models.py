from fundooapp import db, ma


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.username, self.email, self.password)


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
