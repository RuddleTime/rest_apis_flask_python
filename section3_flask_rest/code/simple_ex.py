from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Student(Resource):
    # Resource that can only be accessed by the GET method
    def get(self, name):
        return {'student': name}

# Allowing access to student via http://127.0.0.1:5000/student/Puppy
api.add_resource(Student, '/student/<string:name>')


app.run(port=5000)
