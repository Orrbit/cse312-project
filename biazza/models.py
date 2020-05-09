import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    attachment = db.relationship("Attachment", backref="comment")
    likes = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    all_attachments = []
    user_name = 'Anonymous'

    def __repr__(self):
        return '<Attachment %r>' % self.text


class Accounts(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(300))

    def __repr__(self):
        return '<Accounts %r>' % self.email

class Conversation(db.Model):
    __tablename__ = 'conversation'
    id = db.Column(db.Integer, primary_key=True)
    user_owner_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    user_guest_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    messages = db.relationship("Message", back_populates="conversation")

    def __repr__(self):
        return '<Conversation %r>' % self.id

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    conversation = db.relationship("Conversation", back_populates="messages")
    time = db.Column(db.DateTime(), nullable=False)
    text = db.Column(db.Text(), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    

    def __repr__(self):
        return '<Conversation %r>' % self.id


class UserTokens(db.Model):
    __tablename__ = 'user_tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    token_hash = db.Column(db.String(128), unique=True)


class Attachment(db.Model):
    __tablename__ = 'attachment'
    id = db.Column(db.Integer, primary_key=True)
    user_filename = db.Column(db.String(100))
    path = db.Column(db.String(200), unique=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __repr__(self):
        return '<Attachment %r>' % self.path


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    title = db.Column(db.String(200))
    content = db.Column(db.String(1000))
    likes = db.Column(db.Integer)

    def __repr__(self):
        return '<Question %r>' % self.title
