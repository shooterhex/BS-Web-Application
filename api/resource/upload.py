import os
from os import path
import shutil
import datetime
from PIL import Image
from flask_restful import Resource
from flask import redirect, request
from flask_login import current_user
from api.resource import status

class UploadPicture(Resource):
    """实体名称消歧联想"""

    def get(self):
        """
            上传图片，保存到服务器本地
            文件对象保存在request.files上，并且通过前端的input标签的name属性来获取
            :return: 重定向到主页
            """
        photos = request.files.getlist("f1")
        if not photos[0].filename:
            print('No selected file.')
            return redirect("/")

        # uid = str(current_user.get_id())

        # if 'datasets' in data['user'][uid].keys():
        #     dataset_id = len(data['user'][uid]['datasets']) + 1
        #     os.mkdir("./static/" + uid + str(dataset_id))
        #     os.mkdir("./static/" + uid + str(dataset_id) + "/images/")
        #     os.mkdir("./static/" + uid + str(dataset_id) + "/thumb/")
        # else:
        #     os.mkdir("./static/" + uid)
        #     os.mkdir("./static/" + uid + "/1")
        #     os.mkdir("./static/" + uid + "/1/images/")
        #     os.mkdir("./static/" + uid + "/1/thumb/")

        for photo in photos:
            now_date = datetime.datetime.now()
            # uid = now_date.strftime('%Y-%m-%d-%H-%M-%S')
            # 保存文件到服务器本地

            file = "./static/" + status.working_path + "/images/" + photo.filename
            photo.save(file)

            with open(file, 'rb') as f:
                if len(f.read()) < 100:
                    os.remove(file)
                    pass
                else:
                    im = Image.open(file)
                    x, y = im.size
                    y_s = int(y * 174 / x)

                    out = im.resize((174, y_s), Image.ANTIALIAS)

                    uid2 = now_date.strftime('%Y-%m-%d-%H-%M-%S')
                    # 保存文件到服务器本地
                    file2 = "./static/" + status.working_path + "/thumb/" + photo.filename
                    if len(out.mode) == 4:
                        r, g, b, a = out.split()
                        img = Image.merge("RGB", (r, g, b))
                        img.convert('RGB').save(file2, quality=10)
                    else:
                        out.save(file2)
        else:
            print('没有选择文件')
        return redirect("/workspace")

    def post(self):
        return self.get()
