import os
from os import path
import datetime
from flask_restful import Resource
from flask import render_template, make_response, request
from flask_login import current_user

class GetWorkspace(Resource):
    """主页
    """

    def get(self):
        if current_user.is_authenticated:
            uid = current_user.get_id()
            if path.exists('./static/' + str(uid) + '/thumb/'):
                pic_li = os.listdir('./static/' + str(uid) + '/thumb/')
            else:
                pic_li = None
        else:
            pic_li = None
        # pic_li.sort(reverse=True)
        a = datetime.datetime.now()
        a = a + datetime.timedelta(0)
        time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
        context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
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
