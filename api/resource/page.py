import os
import datetime
from flask_restful import Resource
from flask import render_template, make_response, request


class GetIndex(Resource):
    """主页
    """

    def get(self):
        pic_li = os.listdir('./static/img/images/')
        pic_li.sort(reverse=True)
        a = datetime.datetime.now()
        a = a + datetime.timedelta(0)
        time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
        context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
        return make_response(render_template('index.html', context=context))

    def post(self):
        return self.get()


class GetRecycleBin(Resource):
    """回收站
    """
    def get(self):
        pic_li = os.listdir('./static/img/recycle/')
        pic_li.sort(reverse=True)
        a = datetime.datetime.now()
        a = a + datetime.timedelta(0.5)
        time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
        context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
        return make_response(render_template('recycle.html', context=context))

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