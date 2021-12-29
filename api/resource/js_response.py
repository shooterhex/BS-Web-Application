import os
import random
import shutil
from PIL import Image
from flask import request, redirect
from flask_restful import Resource
from flask_login import current_user
from api.resource import status
import json

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
        imgs_li = os.listdir('./static/' + str(uid) + '/thumb')

        if current_user.is_authenticated:
            pic_name = request.form.get('name')
            if pic_name in imgs_li:
                file_name = './static/' + str(uid) + '/images/%s' % pic_name
                thumb_name = './static/' + str(uid) + '/thumb/%s' % pic_name
                os.remove(file_name)
                os.remove(thumb_name)
                return "200"
            else:
                return '401'
        else:
            return '401'

    def post(self):
        return self.get()


class Revolve(Resource):
    def get(self):
        """
        旋转图片，将图片存到images文件夹里
        :return: 200
        """
        pic_name = request.form.get('name')
        pw = request.form.get('pw')
        uid = current_user.get_id()
        imgs_li = os.listdir('./static/' + str(uid) + '/images')
        print(pic_name, imgs_li, pw, pic_name)
        if pic_name in imgs_li and pw == 'admin':
            file_name = './static/' + str(uid) + '/images/%s' % pic_name
            img = Image.open(file_name)  # 打开图片
            img3 = img.transpose(Image.ROTATE_90)  # 旋转 90 度角。
            img3.save(file_name)
            return "200"
        else:
            return "401"

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
        favorite_num = random.randrange(1, 5)
        reference_num = random.randrange(2000)

        with open("./static/json/user_data.json", 'r+') as json_fp:
            data = json.load(json_fp)
            if 'datasets' in data['user'][uid].keys():
                if tag != '':
                    dataset = {'dataset_id': len(data['user'][uid]['datasets']) + 1,
                               'dataset_name': name,
                               'dataset_tag': tag,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}
                else:
                    dataset = {'dataset_id': len(data['user'][uid]['datasets']) + 1,
                               'dataset_name': name,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}
            else:
                data['user'][uid]['datasets'] = []
                if tag != '':
                    dataset = {'dataset_id': 1,
                               'dataset_name': name,
                               'dataset_tag': tag,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}
                else:
                    dataset = {'dataset_id': 1,
                               'dataset_name': name,
                               'dataset_fav': favorite_num,
                               'dataset_ref': reference_num}

            data['user'][uid]['datasets'].append(dataset)
            json_fp.seek(0, 0)
            json.dump(data, json_fp)

        status.isRemove = False

        return "200"

    def post(self):
        return self.get()