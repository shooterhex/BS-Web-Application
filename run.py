from flask import Flask
from api import bp
from api.resource.account import db, login_manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/')
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\asus\\Desktop\\BS\\myproj\\database\\database.db'
bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

if __name__ == '__main__':
    # 生产状态可以把debug调成False
    db.init_app(app)
    login_manager.init_app(app)
    app.run(host='127.0.0.1', port=80, debug=True)
