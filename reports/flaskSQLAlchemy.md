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

  FILL ME OUT
  
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

  The key responsility of the models.py file is to layout how the python objects are going to be mapped to a sql
  
 ### CRUD

FILL ME OUT
  
## How is flask completing these three tasks?
 
### Connecting to the Database
  
  The primary point the URI is recieved in the SQLAlchemy Library is [create_engine](https://github.com/sqlalchemy/sqlalchemy/blob/ae26007d52caab1575a9aef4fecb90785f7e118d/lib/sqlalchemy/engine/create.py#L45)
  Since this is a flexible library, SQLAlchemy then proceeds to turn the URI passed in into a bunch of connection arguments. For every kind of
  SQL Server it accepts, it has an abstraction layer of the Dialect. Since we are using MySQL with the MySQLConnector, it will get routed to
  [its dialect](https://github.com/sqlalchemy/sqlalchemy/blob/ae26007d52caab1575a9aef4fecb90785f7e118d/lib/sqlalchemy/dialects/mysql/mysqldb.

FILL ME OUT

### Declaring Models
   FILL ME OUT
   
   
### CRUD 
   
  FILL ME OUT
  
  ## Is there any licensing?
  
    The code for this is covered by the MIT License.

FILL ME OUT
    
