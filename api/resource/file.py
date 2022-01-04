import traceback
from flask_restful import Resource
from flask import send_file, request, Response, redirect
from flask_login import current_user
from PIL import Image
import PIL
import json
import simplejson
from werkzeug.utils import secure_filename
from api.resource.frame_extract import frame_extract
from api.resource import status
import os

ALLOWED_EXTENSIONS = {'txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx', 'mp4'}
IGNORED_FILES = {'.gitignore'}


class Robots(Resource):
    def get(self):
        return send_file('./static/favicon/robots.txt')

    def post(self):
        return self.get()


class Favicon(Resource):
    def get(self):
        return send_file('./static/favicon/favicon.ico')

    def post(self):
        return self.get()


class Picture(Resource):
    def get(self):
        pic_name = request.args.get('name')
        file = request.args.get('file')
        file_name = '%s/%s/%s' % (status.working_path, file, pic_name)
        with open(file_name, 'rb') as f:
            content = f.read()
        return Response(content, mimetype="image/jpeg")

    def post(self):
        return self.get()


class LoginAvatar(Resource):
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


class uploadfile():
    def __init__(self, name, type=None, size=None, not_allowed_msg='', is_refresh=False):
        self.name = name
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = "%s/images/%s" % (status.working_path, name)
        self.thumbnail_url = "thumbnail/%s" % name
        self.delete_url = "delete/%s" % name
        self.delete_type = "DELETE"
        self.is_refresh = is_refresh

    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False

    def get_file(self):
        if self.type is not None:
            # POST an image
            if self.is_refresh:
                return {"refresh": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": self.size, }
            elif self.type.startswith('image'):
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "url": self.url,
                        "thumbnailUrl": self.thumbnail_url,
                        "deleteUrl": self.delete_url,
                        "deleteType": self.delete_type, }

            # POST an normal file
            elif self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "url": self.url,
                        "deleteUrl": self.delete_url,
                        "deleteType": self.delete_type, }

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": self.size, }

        # GET image from disk
        elif self.is_image():
            return {"name": self.name,
                    "size": self.size,
                    "url": self.url,
                    "thumbnailUrl": self.thumbnail_url,
                    "deleteUrl": self.delete_url,
                    "deleteType": self.delete_type, }

        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": self.size,
                    "url": self.url,
                    "deleteUrl": self.delete_url,
                    "deleteType": self.delete_type, }


class GetVideoImages(Resource):
    def get(filename):
        return send_file(status.working_path + '/images/' + filename)


class GetVideoThumbs(Resource):
    def get(self, filename):
        return send_file(status.working_path + '/thumb/' + filename)


class DeleteVideoImage(Resource):
    def delete(self, filename):
        file_path = os.path.join(status.working_path, 'images', filename)
        file_thumb_path = os.path.join(status.working_path, 'thumb', filename)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)

                if os.path.exists(file_thumb_path):
                    os.remove(file_thumb_path)

                return simplejson.dumps({filename: 'True'})
            except:
                return simplejson.dumps({filename: 'False'})


class UploadVideo(Resource):
    def get(self):
        # get all file in ./data directory
        files = [f for f in os.listdir(status.working_path + '/images') if
                 os.path.isfile(os.path.join(status.working_path, 'images', f)) and f not in IGNORED_FILES]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(status.working_path, 'images', f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return {"files": file_display}

    def post(self):
        files = request.files['file']

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(status.working_path,
                                                  filename)
                files.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                frame_extract(uploaded_file_path, status.working_path)

                os.remove(uploaded_file_path)
                result = uploadfile(name=filename, type=mime_type, size=size,
                                    not_allowed_msg='视频关键帧已提取，请重新刷新页面！',
                                    is_refresh=True)

            return {"files": [result.get_file()]}

        return redirect('/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    i = 1
    while os.path.exists(os.path.join(status.working_path, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join('data', image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join('data/thumbnail', image))

        return True

    except:
        print(traceback.format_exc())
        return False
