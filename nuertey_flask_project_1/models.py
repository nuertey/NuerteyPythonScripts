from .app import db
import string
import secrets
from datetime import datetime

DATE_FMT = '%d/%m/%Y %H:%M:%S'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    note = db.Column(db.Unicode)
    creation_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship("Profile", back_populates='tasks')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'creation_date': self.creation_date.strftime(DATE_FMT),
            'due_date': self.due_date.strftime(DATE_FMT) if self.due_date else None,
            'completed': self.completed,
            'profile_id': self.profile_id
        }

    def __repr__(self):
        return "<Task: {} | owner: {}>".format(self.name, self.profile.username)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.Unicode, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.Unicode, nullable=False)
    tasks = db.relationship("Task", back_populates='profile', lazy=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_joined = datetime.now()
        self.token = secrets.token_urlsafe(64)

    def to_dict(self):
        """Get the object's properties as a dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined.strftime(DATE_FMT),
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def __repr__(self):
        return "<Profile: {} | tasks: {}>".format(self.username, len(self.tasks))

# Because the model definition occupies a different conceptual space than 
# the application configuration, make models.py to hold model definitions 
# separate from app.py. The Task model should be constructed to have the 
# following attributes:
# 
#     id: a value that's a unique identifier to pull from the database
#     name: the name or title of the task that the user will see when the 
#           task is listed
#     note: any extra comments that a person might want to leave with their 
#           task
#     creation_date: the date and time the task was created
#     due_date: the date and time the task is due to be completed (if at all)
#     completed: a way to indicate whether or not the task has been completed
# 
# Given this attribute list for Task objects, the application's Task object 
# can be defined like so:

# Note the extension of the class constructor method. At the end of the 
# day, any model you construct is still a Python object and therefore must 
# go through construction in order to be instantiated. It's important to 
# ensure that the creation date of the model instance reflects its actual 
# date of creation. You can explicitly set that relationship by effectively 
# saying, "when an instance of this model is constructed, record the date 
# and time and set it as the creation date."
#class Task(db.Model):
#    """Tasks for the To Do list."""
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.Unicode, nullable=False)
#    note = db.Column(db.Unicode)
#    creation_date = db.Column(db.DateTime, nullable=False)
#    due_date = db.Column(db.DateTime)
#    completed = db.Column(db.Boolean, default=False)
#
#    def __init__(self, *args, **kwargs):
#        """On construction, set date of creation."""
#        super().__init__(*args, **kwargs)
#        self.creation_date = datetime.now()

# Similarly, build the User object:
#class User(db.Model):
#    """The User object that owns tasks."""
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.Unicode, nullable=False)
#    email = db.Column(db.Unicode, nullable=False)
#    password = db.Column(db.Unicode, nullable=False)
#    date_joined = db.Column(db.DateTime, nullable=False)
#    token = db.Column(db.Unicode, nullable=False)
#
#    def __init__(self, *args, **kwargs):
#        """On construction, set date of creation."""
#        super().__init__(*args, **kwargs)
#        self.date_joined = datetime.now()
#        # Return a random URL-safe text string, containing nbytes random
#        # bytes. The text is Base64 encoded, so on average each byte results
#        # in approximately 1.3 characters. If nbytes is None or not supplied, 
#        # a reasonable default is used.
#        self.token = secrets.token_urlsafe(64)

# In a given web application, relationships between objects can be  
# expressed thus. In the To-Do List, for example, users own multiple 
# tasks, and each task is owned by only one user. This is an example of 
# a "many-to-one" relationship, also known as a foreign key relationship, 
# where the tasks are the "many" and the user owning those tasks is the
# "one."
#
# In Flask, a many-to-one relationship can be specified using the 
# db.relationship function:

# In setting up the foreign key relationship, for the "many," set fields
# for the user_id of the User that owns this task, as well as the user 
# object with that ID. Also make sure to include a keyword argument
# (back_populates) that updates the User model when the task gets a user
# as an owner.
#user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#user = db.relationship("user", back_populates="tasks")

# For the "one," set a field for the tasks the specific user owns. Similar
# to maintaining the two-way relationship on the Task object, set a keyword
# argument on the User's relationship field to update the Task when it is 
# assigned to a user.
#tasks = db.relationship("Task", back_populates="user")
