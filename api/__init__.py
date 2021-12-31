from flask import Blueprint
from flask_restful import Api

from .resource.upload import UploadPicture
from .resource.page import GetWorkspace, GetDetail, GetWorkspaceVideo
from .resource.file import Robots, Favicon, Picture, LoginAvatar,\
                            GetAvatar, UploadVideo, GetVideoImages,\
                            GetVideoThumbs, DeleteVideoImage
from .resource.js_response import DeletePicture, NameDataset, DeleteDataset
from .resource.account import Login, Signup, Logout
from .resource.homepage import GetIndex, CoverImage
from .resource.annotate import GetTask, Annotate

bp = Blueprint('api', __name__, url_prefix='')
api = Api(bp, catch_all_404s=True)

# 上传图片
api.add_resource(UploadPicture, '/api/upload_row', '/upload_row')
api.add_resource(UploadVideo, '/api/upload', '/upload')

api.add_resource(DeleteVideoImage, '/api/delete/<string:filename>', '/delete/<string:filename>')

# 获取页面
api.add_resource(GetIndex, '/', '/index')
api.add_resource(GetWorkspace, '/api/workspace', '/workspace')
api.add_resource(GetWorkspaceVideo, '/api/workspace_video', '/workspace_video')
api.add_resource(GetDetail, '/api/detail', '/detail')
api.add_resource(GetVideoImages, '/api/data/<string:filename>', '/data/<string:filename>')
api.add_resource(GetVideoThumbs, '/api/thumbnail/<string:filename>', '/thumbnail/<string:filename>')

# 获取静态文件
api.add_resource(Picture, '/api/pic', '/pic')
api.add_resource(LoginAvatar, '/api/login_avatar', '/login_avatar')
api.add_resource(GetAvatar, '/api/avatar', '/avatar')
api.add_resource(Robots, '/api/robots.txt', '/robots.txt')
api.add_resource(Favicon, '/api/favicon.ico', '/favicon.ico')
api.add_resource(CoverImage, '/api/cover', '/cover')

# js操作
api.add_resource(DeletePicture, '/api/delete_pic', '/delete_pic')
api.add_resource(NameDataset, '/api/name_dataset', '/name_dataset')
api.add_resource(DeleteDataset, '/api/delete_dataset', '/delete_dataset')

#注册、登入、登出
api.add_resource(Login, '/api/login', '/login')
api.add_resource(Signup, '/api/signup', '/signup')
api.add_resource(Logout, '/api/logout', '/logout')

api.add_resource(GetTask, '/api/task', '/task')
api.add_resource(Annotate, '/api/annotate', '/annotate')