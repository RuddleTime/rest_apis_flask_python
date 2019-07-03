import sqlite3
from flask_restful import Resource, reqparse


class User:

    def __init__(self, _id, username, password):
        self.id = _id # id is a python keyword so using _id
        self.username = username
        self.password = password


    # Add ability to retrieve user objects from the db
    
    # Making this a class method as we were only referrceing 'User'
    # (now 'cls') and not 'self'
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"

        # parameter must be in form of a tuple
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            # Creating user object if data from row
            user = cls(*row)
            """
            # Instead of doing the below we have used *row
            # to pass in a set of positional arguements above
            user = cls(row[0], row[1], row[2])
            """
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"

        # parameter must be in form of a tuple
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row:
            # Creating user object if data from row
            user = cls(*row)
            """
            # Instead of doing the below we have used *row
            # to pass in a set of positional arguements above
            user = cls(row[0], row[1], row[2])
            """
        else:
            user = None

        connection.close()
        return user

# User class (above) must not be the same as the resource we use to let users sign up
# Making this a 'Resource' so it can be added to the API using Flask RESTful
# This could also be done by creating a resource endpoint
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank"
    ) 
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank"
    ) 
    # This will be called when we post some data to the user register
    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        
        if User.find_by_username(username):
            return {'message': "User already exists"}, 400
        
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        # NULL since user id is auto incremented
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()

        return {'message': 'User created successfully'}, 201


