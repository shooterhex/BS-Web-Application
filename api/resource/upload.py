import os
from PIL import Image
from flask_restful import Resource
from flask import redirect, request
from api.resource import status


class UploadPicture(Resource):
    def get(self):
        photos = request.files.getlist("f1")
        if not photos[0].filename:
            print('No selected file.')
            return redirect("/")

        for photo in photos:
            file = status.working_path + "/images/" + photo.filename
            photo.save(file)
            self.save_thumb(file, photo.filename)
        else:
            print('没有选择文件')

        return redirect("/workspace")

    def post(self):
        return self.get()

    @staticmethod
    def save_thumb(file, name):
        with open(file, 'rb') as f:
            if len(f.read()) < 100:
                os.remove(file)
                pass
            else:
                im = Image.open(file)
                x, y = im.size
                y_s = int(y * 174 / x)

                out = im.resize((174, y_s), Image.ANTIALIAS)

                # 保存文件到服务器本地
                file2 = status.working_path + "/thumb/" + name
                if len(out.mode) == 4:
                    r, g, b, a = out.split()
                    img = Image.merge("RGB", (r, g, b))
                    img.convert('RGB').save(file2, quality=10)
                else:
                    out.save(file2)
