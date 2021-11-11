from flask import Blueprint
from flask_restful import Api

from .resource.upload import UploadPicture
from .resource.page import GetIndex, GetDetail
from .resource.file import Robots, Favicon, Picture
from .resource.index import DeletePicture, Revolve

bp = Blueprint('api', __name__, url_prefix='')
api = Api(bp, catch_all_404s=True)

# 上传图片
api.add_resource(UploadPicture, '/api/upload_row', '/upload_row')

# 获取页面
api.add_resource(GetIndex, '/', '/index')
api.add_resource(GetDetail, '/api/detail', '/detail')

# 获取静态文件
api.add_resource(Picture, '/api/pic', '/pic')
api.add_resource(Robots, '/api/robots.txt', '/robots.txt')
api.add_resource(Favicon, '/api/favicon.ico', '/favicon.ico')

# 主页图片操作
api.add_resource(Revolve, '/api/revolve', '/revolve')
api.add_resource(DeletePicture, '/api/delete', '/delete')

