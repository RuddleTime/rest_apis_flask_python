# Creating user object
# Store of data

class User:
    def __init__(self, _id, username, password):
        self.id = _id # id is a python keyword so using _id
        self.username = username
        self.password = password
