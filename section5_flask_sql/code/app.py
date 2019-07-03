from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# When we import a file (or something from a 
# file), Python runs the file
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemsList

app = Flask(__name__)
# XXX: do not leave secert key visible if publishing code
app.secert_key = "jose"
#app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'boo'
api = Api(app)

# JWT creates a new endpoint -> /auth
# When /auth is called we send it a username and password
# JWT entention sends these to authenticate function and get the corrent object
# Then the password associate with that object is compared to the one recieved from the endpoint 
# If they match the user is returned and becomes the identity
# jwt = JWT(app, authenticate, identity)  # /auth

# Changing the endpoint from /auth to /login, 
# we would:
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

"""
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
"""

# Allowing access to student via http://127.0.0.1:5000/student/Puppy
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')

# Making sure the flask app doesn't run just by
# app.py being imported
# Python assigns __main__ as the name of the file that
# has been run via 'python xxxx.py' command 
if __name__=='__main__':
    app.run(port=5000, debug=True)
