from flask_restful import Api
from apiapp.views.view import ViewResource
from apiapp.views.viewdetail import ViewDetailResource
from apiapp.views.mesdetail import MesDetailResource,DelMesResource
api = Api()   #创建Api对象，靠该对象关联资源类于路由


def init_api(app):
    api.init_app(app)#Api于flask程序实例关联

api.add_resource(ViewResource,'/fatie/')#关联ToyResource资源
api.add_resource(ViewDetailResource,'/fatie/detail/')
api.add_resource(MesDetailResource,'/message/')
api.add_resource(DelMesResource,'/delmes/')