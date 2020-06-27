# Initializing the database
# 
# Now that the models and model relationships are set, start setting up 
# your database. Flask doesn't come with its own database-management 
# utility, so you'll have to write your own (to some degree). You don't 
# have to get fancy with it; you just need something to recognize what 
# tables are to be created and some code to create them (or drop them 
# should the need arise). If you need something more complex, like 
# handling updates to database tables (i.e., database migrations), you'll
#  want to look into a tool like Flask-Migrate or Flask-Alembic.
# 
# Create a script called initializedb.py next to setup.py for managing 
# the database. (Of course, it doesn't need to be called this, but why 
# not give names that are appropriate to a file's function?) Within 
# initializedb.py, import the db object from app.py and use it to create 
# or drop tables. initializedb.py should end up looking something like 
# this:
from nuertey_flask_project_1.app import db
import os

if bool(os.environ.get('DEBUG', '')):
    db.drop_all()
db.create_all()

If a DEBUG environment variable is set, drop tables and rebuild. Otherwise, just create the tables once and you're good to go.
