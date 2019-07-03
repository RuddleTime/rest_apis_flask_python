from werkzeug.security import safe_str_cmp
from user import User

# in memory table of our registered users
users = [
    User(1, "Danny", "guess")
]

# if User wasn't imported, then the below would be required
"""
users = [
    {
        'id': 1,
        'username': 'Danny',
        'password': 'boo'
    }
]
"""

# Mappings help avoid iterating over the users list everytime
username_mapping = {
    u.username: u for u in users
}
userid_mapping = {
    u.id: u for u in users
}

# if User wasn't imported, then the below would be required
"""
username_mapping - {
    'danny': {
        'id': 1,
        'username': 'Danny',
        'password': 'guess'
    }
}

userid_mapping = {
    1: {
        'id': 1,
        'username': 'Danny',
        'password': 'guess'
    }
}
"""

# function to authenticate user
# i.e. given a username and password, select the correct user
def authenticate(username, password):
    # using .get instead of [''], allows us to set a default value
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

# idenity function is unique to flask-JWT
# takes in a payload (contents of JWT token)
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
