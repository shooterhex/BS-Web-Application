from flask_restful import Resource
from flask import Response, render_template, make_response, redirect

class CoverImage(Resource):
    def get(self):
        file_name = './static/public_img/cover/cover.jpg'
        with open(file_name, 'rb') as f:
            content = f.read()
        return Response(content, mimetype='image/jpeg')

    def post(self):
        return self.get()

class GetIndex(Resource):
    def get(self):
        return make_response(render_template('index.html'))

    def post(self):
        return self.get()