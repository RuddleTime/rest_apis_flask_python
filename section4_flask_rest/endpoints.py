from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


stores = [
    {
        'name': 'Christina\'s Store',
        'items': [
            {
                'name': 'Kitten',
                'price': 19.99
            }
        ]
    },
    {
        'name': 'Danny\'s Store',
        'items': [
            {
                'name': 'Bear',
                'price': 119.99
            }
        ]
    }
]

# We are not a browser, we are thinking from the server side
# POST - used to recieve data
# GET - used to send data back only

# Endpoint being created:


@app.route('/')
def home():
    return render_template('index.html')


# POST /store data: {name:} - create a store with a given name
@app.route('/store', methods=['POST'])
def create_store():
    # request here is the request that was made to this ('/store') endpoint
    # get_json - this will convert the json string into a python dict
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name> - get a store with a given name, return data about it
@app.route('/store/<string:name>')
def get_store(name):
    for item in stores:
        if item['name']==name:
            return jsonify(item)
    return jsonify({'message': 'Store not found'.format(name)})

# GET /store - return list of all stores
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores}) # convert the stores variable into JSON


# POST /store/<string:name>/item {name:, price} - create item for a specific store
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name']==name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store not found'})


# GET /store/<string:name>/item - get all items in specific store
@app.route('/store/<string:name>/items')
def get_items_in_store(name):
    for store in stores:
        if store['name']==name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Store not found'})

app.run(port=5000)

