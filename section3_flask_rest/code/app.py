from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

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
jwt = JWT(app, authenticate, identity)

items = [
    {'name': 'bed', 'price': 10.21}
]


class Item(Resource):
    # Below makes parser belong to the Item class 
    # not an individual method
        
    # making sure that only some elements can be passed in
    # through the json payload
    # e.g. we should not be able to change the item name
    # setting up parser
    parser = reqparse.RequestParser()
    # parsing will look in json payload, but also form payloads
    # defining arguements
    parser.add_argument(
        'price',
        type=float,
        required=True, #no request can come through without price
        help="This field cannot be blank"
        )

    # Resource that can only be accessed by the GET method
    @jwt_required()  # So we have to authenticate before calling GET method
    def get(self, name):
        # filter function returns a filter object (not a list or dict etc.)
        # next -> will give the first item found by filter function
        # next -> will raise an error if there are no items
        # found, so defaulting to None
        item = next(filter(lambda x: x['name']==name, items), None)
        return {'item': item}, 200 if item else 404
        """
        Above is simplication of the below:

        for item in items:
            if item['name']==name:
                return item
        return {'item': get}, 404
        """

    def post(self, name):
        """
        # Using 'force=True' means we do not need the content type set,
        # can be dangerous
        # Can use 'silent=True' this will not give an error, but will 
        # just return None
        data = request.get_json()
        """

        data = Item.parser.parser_args()
        # Checking if item already exists
        if next(filter(lambda x: x['name']==name, items), None) is not None:
            return {
                "message": "Item with name '{0}' already exists".format(name)
        }, 400
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    def put(self, name):  # idempotence action
        # only the vaild values from the payload will be put in 'data' variable
        data = Item.parser.parser_args()
        """
        Would use the below if not using parser
        data = request.get_json()
        """
        # check if item already exists
        item = next(filter(lambda x: x['name']==name, items), None)
        # if item does not exists, create the item
        if item is None:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        # otherwise update the item
        else:
            item.update(data)
        return item 

    def delete(self, name):
        """
        new_items = []
        for item in items:
            if item['name']!=name:
                new_items.append(item)
        if len(new_items) == len(items):
            return {'message': 'Item not found'}
        else:
            items = new_items #XXX: needs to be overwitten globally
            return {'message': 'Items deleted'}
        """
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {'message': 'Item deleted'}


class ItemsList(Resource):
    def get(self):
        return {'items': items}

# Allowing access to student via http://127.0.0.1:5000/student/Puppy
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')


app.run(port=5000, debug=True)
