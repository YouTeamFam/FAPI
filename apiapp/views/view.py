from flask_restful import Resource, marshal_with, fields, marshal
from flask_restful.reqparse import RequestParser
from flask import request
from apiapp.models import TUserPost

rp1 = RequestParser()
view_output_instance = {
    "user_id": fields.Integer(attribute="id"),
    "sex": fields.String(attribute="sex"),
    "phone": fields.String(attribute="phone"),
    "Avatar_path": fields.String(attribute="Avatar_path"),
    "u_name": fields.String(attribute="u_name"),
}
view_output1 = {
    "post_id": fields.Integer(attribute="post_id"),
    "title": fields.String(attribute="title"),
    "content": fields.String(attribute="content"),
    "date": fields.DateTime(attribute="date"),
    "tie_pic": fields.String(attribute="tie_pic"),
    "user": fields.Nested(view_output_instance)
}
view_output = {
    "code": fields.String,
    "msg": fields.String,
    "data": fields.List(fields.Nested(view_output1))   # ties为一个列表
}
class ViewResource(Resource):
    def get(self):
        print("请求成功*******************")
        a = request.args.get("pageCode")
        b = request.args.get("limitNum")
        a = int(a)
        b = int(b)
        ties = TUserPost.query.all()[a:b]
        data = {
            "code": "666",
            "msg": '查询成功',
            "data": ties
        }
        return marshal(data, view_output)

