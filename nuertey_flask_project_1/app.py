import os
import sys
import json
from datetime import datetime
from flask import Flask
from flask import jsonify
from flask import request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from functools import wraps
from passlib.hash import pbkdf2_sha256 as hasher

# An app object is an instance of the Flask object. It'll act as the central 
# configuration object for the entire application. It's used to set up pieces 
# of the application required for extended functionality, e.g., a database 
# connection and help with authentication.
app = Flask(__name__)

# It's regularly used to set up the routes that will become the application's 
# points of interaction. To explain what this means, let's look at the code 
# it corresponds to.

# Views and URL config
# 
# The last bits needed to connect the entire application are the views and
# routes. In web development, a "view" (in concept) is functionality that 
# runs when a specific access point (a "route") in your application is hit. 
# These access points appear as URLs: paths to functionality in an application 
# that return some data or handle some data that has been provided. The 
# views will be logical structures that handle specific HTTP requests from 
# a given client and return some HTTP response to that client.
# 
# In Flask, views appear as functions; for example, see the hello_world 
# view below.
#
# With Flask, a function is marked as a view when it is decorated by 
# app.route. In turn, app.route adds to the application's central 
# configuration a map from the specified route to the function that runs 
# when that route is accessed. You can use this to start building out the 
# rest of the API.
@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

# This is the most basic complete Flask application. app is an instance of 
# Flask, taking in the __name__ of the script file. This lets Python know 
# how to import from files relative to this one. 
# 
# Any view you specify must be decorated by app.route to be a functional 
# part of the application. You can have as many functions as you want 
# scattered across the application, but in order for that functionality to 
# be accessible from anything external to the application, you must decorate 
# that function and specify a route to make it into a view.
# 
# In the example above, when the app is running and accessed at 
# http://domainname/, a user will receive "Hello, World!" as a response.

# Note that a wide variety of SQL database management systems can be used 
# with flask-sqlalchemy, as long as the DBMS has an intermediary that 
# follows the DBAPI-2 standard. In this example, I'll use PostgreSQL 
# (mainly because I've used it a lot), so the intermediary to talk to the 
# Postgres database is the psycopg2 package. Make sure psycopg2 is installed 
# in your environment and include it in the list of required packages in 
# setup.py. You don't have to do anything else with it; flask-sqlalchemy 
# will recognize Postgres from the database URL.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
auth = HTTPTokenAuth(scheme='Token')
db = SQLAlchemy(app)

# Beware of circular dependency by ensuring that the db is created first
# before importing the models.
from .models import Task, Profile

INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'

# Start with a view that handles only GET requests, and respond with the 
# JSON representing all the routes that will be accessible and the methods 
# that can be used to access them.

# Note that, on its own, Flask supports routing to exactly matching URIs, 
# so accessing that same route with a trailing / would create a 404 error. 
# If you wanted to handle both with the same view function, you'd need 
# stack decorators like the below.
#
# An interesting case is that if the defined route had a trailing slash 
# and the client asked for the route without the slash, you wouldn't need 
# to double up on decorators. Flask would redirect the client's request
# appropriately. It's odd that it doesn't work both ways.
#@app.route('/api/v1', methods=["GET"])
#@app.route('/api/v1/', methods=["GET"])
#def info_view():
#    """List of routes for this API."""
#    # A good structure that contains complexity but can still be stringified is a Python dictionary. Therefore, I recommend that, whenever you want to send some data to the client, you choose a Python dict with whatever key-value pairs you need to convey information. To turn that dictionary into a properly formatted JSON response, headers and all, pass it as an argument to Flask's jsonify function (from flask import jsonify).
#    output_dictionary = {
#        'info': 'GET /api/v1',
#        'register': 'POST /api/v1/accounts',
#        'single profile detail': 'GET /api/v1/accounts/<username>',
#        'edit profile': 'PUT /api/v1/accounts/<username>',
#        'delete profile': 'DELETE /api/v1/accounts/<username>',
#        'login': 'POST /api/v1/accounts/login',
#        'logout': 'GET /api/v1/accounts/logout',
#        "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
#        "create task": 'POST /api/v1/accounts/<username>/tasks',
#        "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
#        "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
#        "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
#    }
#    return jsonify(output_dictionary)

# The next thing is that Flask's route patterns can have a bit more nuance. 
# One scenario is a hardcoded route that must be matched perfectly to 
# activate a view function. Another scenario is a route pattern that can 
# handle a range of routes, all mapping to one view by allowing a part 
# of that route to be variable. If the route in question has a variable, 
# the corresponding value can be accessed from the same-named variable 
# in the view's parameter list:
#
# @app.route('/a/sample/<variable>/route')
# def some_view(variable):
#     # some code blah blah blah

#@app.route('/api/v1/accounts/<username>/tasks', methods=['POST'])
#def create_task(username):
#    """Create a task for one user."""
#    # With Flask, you can ask for the User object directly through the query 
#    # attribute for the instance matching your criteria. This type of 
#    # query would provide a list of objects (even if it's only one object 
#    # or none at all), so to get the object you want, just call first().
#    user = User.query.filter_by(username=username).first()
#    if user:
#        # Whenever data is sent to the application, regardless of the 
#        # HTTP method used, that data is stored on the form attribute 
#        # of the request object. The name of the field on the frontend 
#        # will be the name of the key mapped to that data in the form 
#        # dictionary. It'll always come in the form of a string, so if 
#        # you want your data to be a specific data type, you'll have to 
#        # make it explicit by casting it as the appropriate type.
#        task = Task(
#            name=request.form['name'],
#            note=request.form['note'],
#            creation_date=datetime.now(),
#            due_date=datetime.strptime(due_date, INCOMING_DATE_FMT) if due_date else None,
#            completed=bool(request.form['completed']),
#
#            # The other thing to note is the assignment of the current 
#            # user's user ID to the newly instantiated Task. This is how 
#            # that foreign key relationship is maintained.
#            user_id=user.id,
#        )
#
#        # The db.session.add(task) stages the new Task instance to be 
#        # added to the table, but doesn't add it yet. While it's done 
#        # only once here, you can add as many things as you want before 
#        # committing. The db.session.commit() takes all the staged 
#        # changes, or "commits," and applies them to the corresponding 
#        # tables in the database.
#        db.session.add(task)
#        db.session.commit()
#
#        # The response is an actual instance of a Response object with 
#        # its mimetype, body, and status set deliberately. The goal for 
#        # this view is to alert the user they created something new. 
#        # Seeing how this view is supposed to be part of a backend API 
#        # that sends and receives JSON, the response body must be JSON 
#        # serializable. A dictionary with a simple string message should 
#        # suffice. Ensure that it's ready for transmission by calling 
#        # json.dumps on your dictionary, which will turn your Python 
#        # object into valid JSON. This is used instead of jsonify, as 
#        # jsonify constructs an actual response object using its input 
#        # as the response body. In contrast, json.dumps just takes a 
#        # given Python object and converts it into a valid JSON string 
#        # if possible.
#        output = {'msg': 'posted'}
#        response = Response(
#            mimetype="application/json",
#            response=json.dumps(output),
#
#            # By default, the status code of any response sent with Flask 
#            # will be 200. That will work for most circumstances, where 
#            # you're not trying to send back a specific redirection-level 
#            # or error-level message. Since this case explicitly lets the 
#            # frontend know when a new item has been created, set the 
#            # status code to be 201, which corresponds to creating a new 
#            # thing.
#            status=201
#        )
#        return response

# 200 OK
#     The request has succeeded. The meaning of the success depends on the HTTP method:
# 
#         GET: The resource has been fetched and is transmitted in the message body.
#         HEAD: The entity headers are in the message body.
#         PUT or POST: The resource describing the result of the action is transmitted in the message body.
#         TRACE: The message body contains the request message as received by the server
# 
# 201 Created
#     The request has succeeded and a new resource has been created as a result. This is typically the response sent after POST requests, or some PUT requests.
# 

def forbidden_response():
    """Return an HTTP response when the user is forbidden."""
    response = Response(
        mimetype="application/json",
        response=json.dumps({'error': 'You do not have permission to access this profile.'}),
        status=403
    )
    return response


def notfound_response():
    """Return an HTTP response when a nonexistant profile has been searched for."""
    response = Response(
        mimetype="application/json",
        response=json.dumps({'error': 'The profile does not exist'}),
        status=404
    )
    return response

def get_profile(username):
    """Check if the requested profile exists."""
    return Profile.query.filter_by(username=username).first()


@auth.verify_token
def verify_token(token):
    """Verify that the incoming request has the expected token."""
    if token:
        username = token.split(':')[0]
        profile = get_profile(username)
        return token == profile.token


def authenticate(response, profile):
    """Authenticate an outgoing response with the user's token."""
    token = f'{profile.username}:{profile.token}'
    response.set_cookie('auth_token', value=token)
    return response


@app.route('/api/v1')
def index():
    """List of routes for this API."""
    output = {
        'info': 'GET /api/v1',
        'register': 'POST /api/v1/accounts',
        'single profile detail': 'GET /api/v1/accounts/<username>',
        'edit profile': 'PUT /api/v1/accounts/<username>',
        'delete profile': 'DELETE /api/v1/accounts/<username>',
        'login': 'POST /api/v1/accounts/login',
        'logout': 'GET /api/v1/accounts/logout',
        "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
        "create task": 'POST /api/v1/accounts/<username>/tasks',
        "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
        "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
        "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
    }
    response = jsonify(output)
    return response


@app.route('/api/v1/accounts', methods=['POST'])
def register():
    """Add a new user profile if it doesn't already exist."""
    needed = ['username', 'email', 'password', 'password2']
    if all([key in request.form for key in needed]):
        username = request.form['username']
        profile = get_profile(username)
        if not profile:
            if request.form['password'] == request.form['password2']:
                new_profile = Profile(
                    username=username,
                    email=request.form['email'],
                    password=hasher.hash(request.form['password']),
                )
                db.session.add(new_profile)
                db.session.commit()

                response = Response(
                    response=json.dumps({"msg": 'Profile created'}),
                    status=201,
                    mimetype="application/json"
                )
                return authenticate(response, new_profile)

            response = jsonify({"error": "Passwords don't match"})
            response.status_code = 400
            return response

        response = jsonify({'error': f'Username "{username}" is already taken'})
        response.status_code = 400
        return response

    response = jsonify({'error': 'Some fields are missing'})
    response.status_code = 400
    return response


@app.route('/api/v1/accounts/login', methods=['POST'])
def login():
    """Authenticate a user."""
    needed = ['username', 'password']
    if all([key in request.forms for key in needed]):
        profile = get_profile(request.forms['username'])
        if profile and hasher.verify(request.forms['password'], profile.password):
            response = Response(
                response=json.dumps({'msg': 'Authenticated'}),
                mimetype="application/json",
                status=200
            )
            return authenticate(response, profile)
        response.status_code = 400
        return {'error': 'Incorrect username/password combination.'}
    response.status_code = 400
    return {'error': 'Some fields are missing'}


@app.route('/api/v1/accounts/logout', methods=["GET"])
def logout():
    """Log a user out."""
    return jsonify({'msg': 'Logged out.'})


@app.route('/api/v1/accounts/<username>', methods=["GET"])
@auth.login_required
def profile_detail(username):
    """Get the detail for an individual profile."""
    profile = get_profile(username)
    if profile:
        response = Response(
            mimetype="application/json",
            response=json.dumps(profile.to_dict()),
        )
        return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks', methods=['GET'])
@auth.login_required
def task_list(username):
    """List all of the tasks for one user."""
    profile = get_profile(username)
    if profile:
        tasks = [task.to_dict() for task in profile.tasks.all()]
        output = {'username': username, 'tasks': tasks}
        response = Response(
            mimetype="application/json",
            response=json.dumps(output)
        )
        return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks', methods=['POST'])
@auth.login_required
def create_task(username):
    """List all of the tasks for one user."""
    profile = get_profile(username)
    if profile:
        task = Task(
            name=request.form['name'],
            note=request.form['note'],
            creation_date=datetime.now(),
            due_date=datetime.strptime(due_date, INCOMING_DATE_FMT) if due_date else None,
            completed=request.form['completed'],
            profile_id=profile.id,
        )
        db.session.add(task)
        db.session.commit()
        output = {'msg': 'posted'}
        response = Response(
            mimetype="application/json",
            response=json.dumps(output),
            status=201
        )
        return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def task_detail(username, task_id):
    """Get the detail for one task if that task belongs to the provided user."""
    profile = get_profile(username)
    if profile:
        task = Task.query.get(task_id)
        if task in profile.tasks:
            output = {'username': username, 'task': task.to_dict()}
            response = Response(
                mimetype="application/json",
                response=json.dumps(output)
            )
            return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def task_update(username, task_id):
    """Update one task if that task belongs to the provided user."""
    profile = get_profile(username)
    if profile:
        task = Task.query.get(task_id)
        if task in profile.tasks:
            if 'name' in request.form:
                task.name = request.form['name']
            if 'note' in request.form:
                task.note = request.form['note']
            if 'completed' in request.form:
                task.completed = request.form['completed']
            if 'due_date' in request.form:
                due_date = request.form['due_date']
                task.due_date = datetime.strptime(due_date, INCOMING_DATE_FMT) if due_date else None
            db.session.add(task)
            db.session.commit()
            output = {'username': username, 'task': task.to_dict()}
            response = Response(
                mimetype="application/json",
                response=json.dumps(output)
            )
            return authenticate(response, profile)
    return notfound_response()    


@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def task_delete(username, task_id):
    """Delete one task if that task belongs to the provided user."""
    profile = get_profile(username)
    if profile:
        task = Task.query.get(task_id)
        if task in profile.tasks:
            db.session.delete(task)
            db.session.commit()
            output = {'username': username, 'msg': 'Deleted.'}
            response = Response(
                mimetype="application/json",
                response=json.dumps(output)
            )
            return authenticate(response, profile)
    return notfound_response()    
