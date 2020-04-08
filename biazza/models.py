import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    attachment = db.relationship("Attachment", back_populates="comment")
    likes = db.Column(db.Integer)

    def __repr__(self):
        return '<Attachment %r>' % (self.text)

class Attachment(db.Model):
    __tablename__ = 'attachment'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    path = db.Column(db.String(50), unique=True)
    comment = db.relationship("Comment", back_populates="attachment", uselist=False)


    def __repr__(self):
        return '<Attachment %r>' % (self.file)