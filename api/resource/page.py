import os
from os import path
import datetime
from flask_restful import Resource
from flask import render_template, make_response, request
from flask_login import current_user
import json
from api.resource import status

class GetWorkspace(Resource):
    """主页
    """
    def get(self):
        uid = int(current_user.get_id())
        with open("./static/json/user_data.json", 'r') as json_fp:
            data = json.load(json_fp)

        if 'datasets' in data['user'][uid - 1].keys():
            dataset_id = len(data['user'][uid - 1]['datasets']) + 1
        else:
            dataset_id = 1
        uid = str(uid)
        status.working_path = uid + "/" + str(dataset_id)
        if not path.exists('./static/' + uid):
            os.mkdir("./static/" + uid)
        if not path.exists("./static/" + status.working_path):
            os.mkdir("./static/" + status.working_path)
            os.mkdir("./static/" + status.working_path + "/images")
            os.mkdir("./static/" + status.working_path + "/thumb")

        pic_li = os.listdir('./static/' + status.working_path + '/thumb/')
        context = {'li': pic_li}

        return make_response(render_template('workspace.html', context=context))

    def post(self):
        return self.get()
        
class GetDetail(Resource):
    """详情页
    """
    def get(self):
        pic_name = request.args.get("name")
        context = dict()
        context['detail_name'] = pic_name
        return make_response(render_template('detail.html', context=context))

    def post(self):
        return self.get()
