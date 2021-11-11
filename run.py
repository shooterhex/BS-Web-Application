from flask import Flask
from api import bp

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/')


if __name__ == '__main__':
    # 生产状态可以把debug调成False
    app.run(host='127.0.0.1', port=80, debug=True)
