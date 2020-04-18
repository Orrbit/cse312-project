# Flask - A Python micro framework for building web applications

Flask is working as a lightweight framework for us to serve up our web application. It has abstracted away a majority of the challenging
tasks for us. Using this framework, we are able to quickly route requests and serve up the proper responses to our client.

**Flask Documentation** - (https://flask.palletsprojects.com/en/1.1.x/)

**Flask Source Code** - (https://github.com/pallets/flask/)

# Phase 1 & PHASE 2; SEE TEMPLATES

As of Phase 1, we are using flask to listen for, handle, and serve up http requests. These requests are primarily for HTML, CSS, and JS
files. However, it does have the ability to serve up a variety of files such as svgs if we choose to include those.

In this section, we will fully flush out the instances we use Flask in, the why it accomplishes these tasks, and lastly a report of any
licensing that applies with the use of the library

## What is Flask accomplishing for our group?

### Flask Object

  We are using the Flask object throughout our code. Here we can see the initialization of it.
  
https://github.com/Orrbit/cse312-project/blob/master/biazza/__init__.py
  

```python
from flask import Flask

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config.from_object('config')
```

  The parameters passed to the object tell the framework the id of the service and folder paths for both the static and templates. Whenever
  flask gets a request for a file it will search through that directory to see if it can find that file. We are hosting files in this
  directory that provide script functionality and styling. When Clients request a file, Flask will look for it in this directory.
  It is useful to keep these here because it is effectively separating the files by their functionality in the context of web development.
  Files in the templates folder we plan on being able to populate with field based on properties of the requests later on, but for now they 
  are always the same html files getting served up. To clairify, these files are not getting served up unless we specify them.
  
  This leads us to our next point about how we are using Flask for Routing. All of our routing beyond the static files occurs in the
  views.py
  
 ### Routing

https://github.com/Orrbit/cse312-project/blob/master/biazza/views.py
```python
@app.route('/')
def home():
   return render_template("login.html")

@app.route('/home')
def home_page():
   return render_template('home.html')

@app.route('/home/messages')
def messages():
   return render_template('messages.html')

@app.route('/home/questions')
def questions():
   return render_template('questions.html')

@app.route('/home/assignments')
def assignments():
   return render_template('assignments.html')
```

  Here, we are telling the Flask object what function to execute when it recieves a http request with a certain path. For instance,
  when someone is running the server goes to (http://localhost:8000/home), it will fire the home_page function.
  
 ### Rendering templates  
  
  The last thing to touch on that we are currently using Flask for is the rendering templates. The code examples can be seen above.
  As of now, we are not actually using the template functionality, but once we want to implement it, we can use this function to fill
  in variables throghout our html file. For now all we care about is using the render_template function to create a text/html response
  from our server back to the client.
  
  UPDATED FOR THE PHASE 2 RENDERING TEMPLATES
  
  An example that we can see the use of the template engine can be seen in our questions.html inside the templates directory.
  
  ```
  {% for question in questions %}
      {% if loop.index == 1 %}
                        <a class="list-group-item list-group-item-action active" data-toggle="list" role="tab" id="{{question.id}}">      {{question.title}}</a>
      {% else %}
                    <a class="list-group-item list-group-item-action" data-toggle="list" role="tab" id="{{question.id}}">             {{question.title}}</a>
      {% endif %}
  {% endfor %}
                    
  ```
  
  We are giving the html render function a list of questions. Inside eacho one of thes questions, we have an id that we need to assign to the id attribute of our a tag and we also have the question title that will need to be displayed as inner html of the tag. This will help users that are just loading the html page get content that is up to date with what the database has insead of just seeing static content.
  
 ## How is flask completing these three tasks?
 
 ### Flask Object
  
  According to the documentation, the main object that we are using in our code (the Flask object(https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask)) 
  implements a WSGI application. WSGI is a term for a package in python that acts as a server as well as a application side interface.
  Looking into the source code of this object, we can see that it must accomplish tasks that are very similar to the things we have
  learned in lecture.
  
  For example, we can see that the function make_response exists inside of the Flask object. Tracing through this, one will find that
  Flask is creating a response object(which is defined in wrappers.py) and it is populating that response with the return value of a view
  function, the headers, and the status. View this function here [make_response](https://github.com/pallets/flask/blob/29d33203d0325f006c75fc88359872bd68c8bdf5/src/flask/app.py#L2019)
  A little more on this, it is important to note that even Flask uses libraries such as werkzeug (https://palletsprojects.com/p/werkzeug/)
  for packaging up the data.
  
  Another part of the object is the request that comes in. How does flask handle this? Well flask handles the request by passing it into
  it's response class and having the response get augmented depending on the request ([code here](https://github.com/pallets/flask/blob/29d33203d0325f006c75fc88359872bd68c8bdf5/src/flask/app.py#L1955))
  So we will get insight by looking into the werkzeug wrapper. And sure enough if we look into it, we can see that werkzeug wrapper base_request
  includes all of the info about requests that we have covered. There are functions to get the headers, the path, the cookies, query strings,
  potential file streams and form data. Here is the function where we can even see [buffering occuring](https://github.com/pallets/werkzeug/blob/d6e98a0105ea126f10c432d33f101ec793df6440/src/werkzeug/wrappers/base_request.py#L428)
  
   ### Routing
   
   The routing works in flask with the function [add_url_rule](https://github.com/pallets/flask/blob/29d33203d0325f006c75fc88359872bd68c8bdf5/src/flask/app.py#L1178)
   In this function, flask assigns a endpoint to a function. Werkzeug is used as a wrapper once again. The rule class inside of 
   [routing.py](https://github.com/pallets/werkzeug/blob/d6e98a0105ea126f10c432d33f101ec793df6440/src/werkzeug/routing.py#L526)
   This class contains many things we are familiar with such as the endpoints and redirect_to paths. Also it has websocket flags so that
   we be crucial in later phases of the project.
   
   ### Rendering tempalates
   
  Flask is mostly giving us a wrapper class for using jinjas render template. We see that they create a jinja envirornment and then the rest
  is sent off to jinja code. Lets investigate that code. The inner workings have to retrieve the source first and then compile the source
  with all of the information. We don't have to look into how it loads in the info quite yet because we are simply using it to load 
  our source file.
  
  UPDATED FOR THE PHASE 2 RENDERING TEMPLATES
  
  We can see that the jinja template engine is very powerful. A lot of the bulk functionality is in the parser.py function at [here](https://github.com/pallets/jinja/blob/master/src/jinja2/parser.py) If we look at each one of the methods in there, it has a method for parsing each type of statement it could come across, such as parse_for, parse_if and parse_staement. Just as any engine like this is going to work, it has key words that it looks at. It defines the key words that you can use at the [top of the parser](https://github.com/pallets/jinja/blob/da812816ff1a459eefa7ca946b4c108cc7106c85/src/jinja2/parser.py#L8)
  
  ## Is there any licensing?
  
    The authors of this framework comply with the [3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause). The authors
    chalk it up to the users having full utility of it as long as the disclaimer on the code is intact. They also state that users of Flask
    cannot use the name of the authors to endorse the entire product.
