from flask_restful import Resource
from flask import send_file, request, Response
from flask_login import current_user
import json
from api.resource import status

class Robots(Resource):
    """爬虫爬取权限
    """
    def get(self):
        return send_file('./static/favicon/robots.txt')

    def post(self):
        return self.get()


class Favicon(Resource):
    """主页图标
    """
    def get(self):
        return send_file('./static/favicon/favicon.ico')

    def post(self):
        return self.get()


class Picture(Resource):
    """主页图标
    """
    def get(self):
        pic_name = request.args.get('name')
        file = request.args.get('file')
        file_name = './static/%s/%s/%s' % (status.working_path, file, pic_name)
        with open(file_name, 'rb') as f:
            content = f.read()
        return Response(content, mimetype="image/jpeg")

    def post(self):
        return self.get()

class LoginAvatar(Resource):
    """主页图标
    """
    def get(self):
        uid = int(current_user.get_id()) - 1
        with open("./static/json/user_data.json", 'r') as json_fp:
            data = json.load(json_fp)
            avatar_index = str(data['user'][uid]['avatar'])
        file_name = './static/public_img/avatar/avatar' + avatar_index + '_small.png'
        with open(file_name, 'rb') as f:
            content = f.read()
        return Response(content, mimetype="image/jpeg")

    def post(self):
        return self.get()

class GetAvatar(Resource):
    def get(self):
        index = request.args.get('index')
        file_name = './static/public_img/avatar/avatar' + index + '_small.png'
        with open(file_name, 'rb') as f:
            content = f.read()
        return Response(content, mimetype="image/jpeg")

    def post(self):
        return self.get()