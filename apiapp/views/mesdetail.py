from flask_restful import Resource, marshal_with, fields, marshal
from flask_restful.reqparse import RequestParser
from flask import request
from tools.ext import db
from apiapp.models import TUserPost,TUser

rp1 = RequestParser()

view_output1 = {
    "mes_title": fields.String(attribute="mes_title"),
    "mes_text": fields.String(attribute="mes_text"),
    "last_date": fields.DateTime(attribute="last_date"),
    "user_id": fields.Integer(attribute="user_id"),
}
view_output = {
    "code": fields.String,
    "msg": fields.String,
    "data": fields.Nested(view_output1)   # ties为一个列表
}
del_output = {
    "code": fields.String,
    "msg": fields.String,
    "data": fields.Nested(view_output1)   # ties为一个列表
}
class MesDetailResource(Resource):
    def post(self):
        print("请求成功*******************")
        token = request.form.get("token")
        print(token)
        user = TUser.query.filter_by(user_id=3).first()
        print(user.mes_title)
        data = {
            "code": "666",
            "msg": '查询成功',
            "data": user
        }
        return marshal(data, view_output)

class DelMesResource(Resource):
    def get(self):
        print("请求成功*******************")
        user_id = request.args.get("user_id")
        print(user_id)
        user = TUser.query.filter_by(user_id=user_id).first()
        print(user)
        user.mes_title = ""
        user.mes_text = ""
        db.session.add(user)
        db.session.commit()
        print(user.mes_title,user.mes_text)
        data = {
            "code": "666",
            "msg": '删除成功',
        }
        return marshal(data, del_output)