import os
import random
import shutil
from PIL import Image
from flask import request, redirect
from flask_restful import Resource
from flask_login import current_user
from api.resource import status
import json
import shutil

class DeletePicture(Resource):
    # """删除图片，将图片存到回收站
    # """
    # def get(self):
    #     imgs_li = os.listdir('./static/img/images')
    #     pic_name = request.form.get('name')
    #     pw = request.form.get('pw')
    #     if pic_name in imgs_li and pw == 'admin':
    #         file_name = './static/img/images/%s' % pic_name
    #         file_name2 = './static/img/recycle/%s' % pic_name
    #         shutil.move(file_name, file_name2)
    #         return "200"
    #     else:
    #         return "401"

    # def post(self):
    #     return self.get()
    def get(self):
        """
        删除图片的接口，将图片存到清空站
        :return: 200
        """
        uid = current_user.get_id()
        imgs_li = os.listdir('./static/' + status.working_path + '/thumb')

        if current_user.is_authenticated:
            pic_name = request.form.get('name')
            if pic_name in imgs_li:
                file_name = './static/' + status.working_path + '/images/%s' % pic_name
                thumb_name = './static/' + status.working_path + '/thumb/%s' % pic_name
                os.remove(file_name)
                os.remove(thumb_name)
                return "200"
            else:
                return '401'
        else:
            return '401'

    def post(self):
        return self.get()

class NameDataset(Resource):
    def get(self):
        """
        旋转图片，将图片存到images文件夹里
        :return: 200
        """
        name = request.form.get('name')
        tag = request.form.get('tag')
        uid = int(current_user.get_id()) - 1
        favorite_num = random.randrange(6)
        reference_num = random.randrange(2000) + 1
        cover_img = random.randrange(12) + 1

        with open("./static/json/user_data.json", 'r+') as json_fp:
            data = json.load(json_fp)
            if 'datasets' in data['user'][uid].keys():
                if tag != '':
                    dataset = {'dataset_id': len(data['user'][uid]['datasets']) + 1,
                               'dataset_name': name,
                               'dataset_cover': cover_img,
                               'dataset_tag': tag,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}
                else:
                    dataset = {'dataset_id': len(data['user'][uid]['datasets']) + 1,
                               'dataset_name': name,
                               'dataset_cover': cover_img,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}
            else:
                data['user'][uid]['datasets'] = []
                if tag != '':
                    dataset = {'dataset_id': 1,
                               'dataset_name': name,
                               'dataset_cover': cover_img,
                               'dataset_tag': tag,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}
                else:
                    dataset = {'dataset_id': 1,
                               'dataset_name': name,
                               'dataset_cover': cover_img,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}

            data['user'][uid]['datasets'].append(dataset)
            json_fp.seek(0, 0)
            json.dump(data, json_fp)

        return "200"

    def post(self):
        return self.get()

class DeleteDataset(Resource):
    def get(self):
        shutil.rmtree('./static/' + status.working_path)
        return "200"

    def post(self):
        return self.get()