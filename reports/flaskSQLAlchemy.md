# Flask-SQLAlchemy

This is an extension that we use that simplifies the data storage process. It makes interacting with our MySQL database much less complex
and prone to fewer bugs. 

**Flask-SQLAlchemy Documentation** - (https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

**Flask-SQLAlchemy Source Code** - (https://github.com/pallets/flask-sqlalchemy)

# Phase 2

As of Phase 2, we are using this extension to create ORM between python objects and our MySQL structure. Using this library, we enable
developers to do basic CRUD operations on tables quickly and consistently. We have abstracted away the bug prone SQL strings that we
would have to use in python to interact with the database.

In this report, we will fully flush out our use cases for this library and how it accomplishes the communication with our DB. It is
important to note that SQLAlchemy was originally written independent from the flask library, so majority of the code we will dive into
will actually be from here:

**SQLAlchemy Source Code** - https://github.com/sqlalchemy/sqlalchemy

## What is Flask-SQLAlchemy accomplishing for our group?

### Connecting to the Database

  The first thing that this library needs to do to achieve all the other functionality is to connect to a database! Duh! So in the __init__.py
  file, we are doing two critical things with the database; connecting to the MySQL db as well as creating any tables we need. This is done
  at https://github.com/Orrbit/cse312-project/blob/18b470972f5772a80ddf30079cb78d6c75b39a31/biazza/__init__.py#L17
```python
from biazza.models import db

...

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db:3306/biazza'

...

db.init_app(app)
db.create_all()
```

To connect to the database, we are configuring the flask app with the information it needs to know in order to connect. It is given
in the format `mysql://username:password@server:port/db`. The FlaskSQLAlchemy extension will look for the config with the key `SQLALCHEMY_DATABASE_URI`
and then stores this string to pass to SQLAlchemy during engine creation.py#L78)

The second thing happening in the above code snippet is dependant on models, so we will dive into that in the next section.

  

### Declaring Models

  Declaring our models in python with sqlalchemy allows us to have the ORM inside our code that also defines the way the database is setup. Using the comment object as an example below, we are setting up a new table named comment that has 4 columns. An id so we can identify it, the text blob, the likes and then finally a relationship. The relationship lets us define a one to many relationship of comments to attachments, since a comment can have more than one attachment.
  
  https://github.com/Orrbit/cse312-project/blob/18b470972f5772a80ddf30079cb78d6c75b39a31/biazza/models.py#L1
  

```python

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
```

  Using the models.py file, we can easily define our table layout in our mysql database while also defining an easy way in python to interact with every field of the database. We will see this in our CRUD section.
  
 ### CRUD

Now that we have a structure to the data that we are going to send to the database, we can do all the request functionality of the database, often refered to as CRUD operations.

For instance, the way we can Create a comment in our code comes down to three lines of code due to our SQLAlchemy usage.

```python
  comment = Comment(text=form_text, likes=0, question_id=q_id)
  db.session.add(comment)
  db.session.commit()
```

We first create the object that we defined in models.py. This object specifies the text, likes, and question id since we have yet to save the attachements. We then add and commit this. The add will give us the chance to do other "queries" before commiting, similar to how a lock will work in sql. Then, we finally tell the database session to commit the changes we made to the database.

We can see that we are updating the comments likes as well with the following code

```python
  comment = Comment.query.get(data["comment_id"])
  comment.likes = comment.likes + 1
  db.session.commit()
```

Again, 3 lines of code are used to do a quick update of the likes. We are finding the comment by its primary key and then incrementing the likes. Once we commit the changes, we will see that the new number of likes is present in the database.
  
## How is flask completing these three tasks?
 
### Connecting to the Database
  
  The primary point the URI is recieved in the SQLAlchemy Library is [create_engine](https://github.com/sqlalchemy/sqlalchemy/blob/ae26007d52caab1575a9aef4fecb90785f7e118d/lib/sqlalchemy/engine/create.py#L45)
  Since this is a flexible library, SQLAlchemy then proceeds to turn the URI passed in into a bunch of connection arguments. For every kind of
  SQL Server it accepts, it has an abstraction layer of the Dialect. Since we are using MySQL with the MySQLConnector, it will get routed to
  [its dialect](https://github.com/sqlalchemy/sqlalchemy/blob/ae26007d52caab1575a9aef4fecb90785f7e118d/lib/sqlalchemy/dialects/mysql/mysqldb.

The code for sqlalchemy creates an easy way for us to connect to the database, and if we were forced to switch to a new database technology, like Postgres, we could simply change the URI and all of our models and code would still function as expected. SQLAlchemy gives us a really nice, concise way to connect to its database.

### Declaring Models
   We see that the declaring of models is quite simple. The Model class in sqlalchemy flask takes in the object that we are going to be using in the models.py class. In our case of the comments, it is taking in the Comment object. Now since this object is a Model, we will be able to access all of these models when we call the create_all() function in our init.py script. As seen on [this line](https://github.com/pallets/flask-sqlalchemy/blob/706982bb8a096220d29e5cef156950237753d89f/flask_sqlalchemy/__init__.py#L1016), we are getting the metadata of that model we created and we talk with the SQLAlchemy engine to create the table. They create a very streamlined way to do this for all of the tables we have defined in our class.
   
   
### CRUD 
   
  For this we will dive into the db.session.add function that we use for creation.  We will notice that a good amount of error handling and parsing will happend during the add command. The add command is mostly responsible for saving away the object and prepping it to be commited. Isn't acutally putting it in the database yet. We can follow the abstractions in the code all the way to [here](https://github.com/sqlalchemy/sqlalchemy/blob/2f617f56f2acdce00b88f746c403cf5ed66d4d27/lib/sqlalchemy/orm/session.py#L2314). It is saving the object in its state and making sure that the request to add is valid.
  
  For the more important part of this, we can inspect the commit function inside of session.py. The commit function will take us all the way to the engine.py class where it actually starts talking with the database. Once again, the engine will reach into its dialect class to make sure that it uses the language for the proper db type. It then will construct a proper create record based on the ORM and the object we passed into it
  
  ## Is there any licensing?
  
    The code for this is covered by the MIT License.
    
