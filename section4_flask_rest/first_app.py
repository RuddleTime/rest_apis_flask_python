from flask import Flask

# Creating an object of Flask using a unique name
app = Flask(__name__)

# Creating a home page for application and assigning a method to it
@app.route('/') # 'http://www.google.com/'
def home():
    return "Hello world again!"

# Running application
app.run(port=5000)


