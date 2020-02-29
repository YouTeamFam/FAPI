from flask import Flask
from flask_cors import CORS

from apiapp.views.api_views import userblue
from tools import settings
from tools.ext import init_ext


def create_app():
    app = Flask(__name__,static_folder=settings.STATIC_DIR,static_url_path='/s/')
    # app.config['ENV'] = 'developement'  # production
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@120.27.10.187:3306/house1?charset=UTF8MB4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_ext(app)#关联数据库
    app.register_blueprint(userblue, url_prefix='/api/')
    CORS(app)
    return app