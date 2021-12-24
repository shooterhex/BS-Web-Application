from flask_restful import Resource
from flask import current_app, send_file
import os

class Annotate(Resource):
    def get(self):
        dist_dir = current_app.config['VUE_DIR']
        entry = os.path.join(dist_dir, 'index.html')
        return send_file(entry)

    def post(self):
        return self.get()