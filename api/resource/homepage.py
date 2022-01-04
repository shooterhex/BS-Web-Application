from flask_restful import Resource
from flask import Response, render_template, make_response, request
import json


class CoverImage(Resource):
    def get(self):
        cover_index = request.args.get('index')
        file_name = './static/public_img/cover/c' + cover_index + '.jpg'
        with open(file_name, 'rb') as f:
            content = f.read()
        return Response(content, mimetype='image/jpeg')

    def post(self):
        return self.get()


class GetIndex(Resource):
    def get(self):
        with open("./static/json/user_data.json", 'r') as json_fp:
            data = json.load(json_fp)

        return make_response(render_template('index.html', data=data))

    def post(self):
        return self.get()