from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoresList

app = Flask(__name__)
# Telling SQLAlchemy where to find data.db
# Below says the SQLAlchemy database, will live at 
# the root folder of the project
# Note: Below code also by mySQL etc.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Specify a configuration property
# Turns off Flask SQLAlchemy tracker, but not the
# SQLAlchemy tracker - so tracking the extensions behaviours 
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

# XXX: do not leave secert key visible if publishing code
app.secert_key = "jose"
#app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'boo'
api = Api(app)

# SQLAlchemy will create the data.db file automatically, but
# needs to be told what tables and schemas to create in it
# Using a Flask decorator (not from an extension)

@app.before_first_request
def create_tables():
    # Creating tables in data.db (referenced above), if
    # they do not already exist
    db.create_all()

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

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoresList, '/stores')

# Making sure the flask app doesn't run just by
# app.py being imported
# Python assigns __main__ as the name of the file that
# has been run via 'python xxxx.py' command 
if __name__=='__main__':
    # Importing here due to circlar imports
    from db import db
    db.init_app(app)  # the app being pasted in is our flask app
    app.run(port=5000, debug=True)
