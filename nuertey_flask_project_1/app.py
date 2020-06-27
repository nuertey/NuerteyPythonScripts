import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# An app object is an instance of the Flask object. It'll act as the central 
# configuration object for the entire application. It's used to set up pieces 
# of the application required for extended functionality, e.g., a database 
# connection and help with authentication.
app = Flask(__name__)

# It's regularly used to set up the routes that will become the application's 
# points of interaction. To explain what this means, let's look at the code 
# it corresponds to.
@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

# This is the most basic complete Flask application. app is an instance of 
# Flask, taking in the __name__ of the script file. This lets Python know 
# how to import from files relative to this one. The app.route decorator 
# decorates the first view function; it can specify one of the routes used 
# to access the application. (We'll look at this later.)
# 
# Any view you specify must be decorated by app.route to be a functional 
# part of the application. You can have as many functions as you want 
# cattered across the application, but in order for that functionality to 
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
