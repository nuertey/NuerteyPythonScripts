import os
import sys
import json
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

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
db = SQLAlchemy(app)

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
@app.route('/api/v1', methods=["GET"])
@app.route('/api/v1/', methods=["GET"])
def info_view():
    """List of routes for this API."""
    # A good structure that contains complexity but can still be stringified is a Python dictionary. Therefore, I recommend that, whenever you want to send some data to the client, you choose a Python dict with whatever key-value pairs you need to convey information. To turn that dictionary into a properly formatted JSON response, headers and all, pass it as an argument to Flask's jsonify function (from flask import jsonify).
    output_dictionary = {
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
    return jsonify(output_dictionary)

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
