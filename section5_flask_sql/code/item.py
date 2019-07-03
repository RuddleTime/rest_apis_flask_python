import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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

    @jwt_required()  # So we have to authenticate before calling GET method
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item 
        return {'message': 'Item not found'}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        # Only one row should come back, as name is unique
        row = result.fetchone()
        connection.close()

        if row:
            return {
                'item':
                {
                    'name': row[0],
                    'price': row[1]
                }
            }

    @classmethod
    def create_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        
        connection.commit()
        connection.close()

        return None

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit()
        connection.close()

        return None

    # Create
    def post(self, name):
        # Checking if item already exists
        if self.find_by_name(name):
            return {
               "message": "Item with name '{0}' already exists".format(name)
        }, 400 
        
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        
        self.create_item(item)
        
        return item, 201
 
    # Update
    def put(self, name):  # idempotence action
        # only the vaild values from the payload will be put in 'data' variable
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        
        if not self.find_by_name(name): 
            # Create new item
            try:
                self.create_item(item)
            except:
                return {
                    'message': "An error occurred inserting this item"
                }, 500 # Internal server error

        else:
            # Update existing item
            try:
                self.update_item(item)
            except:
                return {
                    'message': 'An error occurred updating the item',
                }, 500
        return item, 201


    # Delete
    def delete(self, name):

        # Checking if item already exists
        if not self.find_by_name(name):
            return {
               "message": "Item with name '{0}' does not exist".format(name)
        }, 400 

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item \'{0}\' deleted'.format(name)}


class ItemsList(Resource):
    # Read
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        #result = cursor.execute(query).fetchall()
        result = cursor.execute(query).fetchall()
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        
        # Don't need to commit as nothing was saved
        # connection.commit()
        
        connection.close()
        return {'items': items}

