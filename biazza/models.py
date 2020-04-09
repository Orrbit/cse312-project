import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    attachment = db.relationship("Attachment", backref="comment")
    likes = db.Column(db.Integer)

    def __repr__(self):
        return '<Attachment %r>' % (self.text)

class Attachment(db.Model):
    __tablename__ = 'attachment'
    id = db.Column(db.Integer, primary_key=True)
    user_filename = db.Column(db.String(100))
    path = db.Column(db.String(200), unique=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))


    def __repr__(self):
        return '<Attachment %r>' % (self.path)