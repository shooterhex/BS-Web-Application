import os

from flask import render_template, make_response, request
from flask_restful import Resource
from api.resource import status

class GetTask(Resource):
    def get(self):
        user_id = str(request.args.get('user'))
        dataset_id = str(request.args.get('dataset'))
        status.working_path = './static/' + user_id + '/' + dataset_id
        pic_li = os.listdir(status.working_path + '/thumb/')
        context = {'li': pic_li}

        return make_response(render_template('task.html', context=context))

    def post(self):
        return self.get()

class Annotate(Resource):
    def get(self):
        pic_name = request.args.get("name")
        context = {'img_name': pic_name}
        return make_response(render_template('annotate.html', context=context))

    def post(self):
        return self.get()