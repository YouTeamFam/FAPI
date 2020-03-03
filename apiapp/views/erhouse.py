from flask_restful import Resource, marshal_with, fields, marshal
from flask_restful.reqparse import RequestParser
from flask import request
from apiapp.models import TSecondSource,TSource

rp1 = RequestParser()

view_output1 = {
    "source_id": fields.Integer(attribute="source_id"),
    "title": fields.String(attribute="title"),
    "hu_type": fields.String(attribute="hu_type"),
    "img_url": fields.String(attribute="img_url"),
    "sum_price": fields.Float(attribute="sum_price"),
    "details": fields.String(attribute="details"),
    "area": fields.String(attribute="area"),
}
view_output = {
    "code": fields.String,
    "msg": fields.String,
    "data": fields.List(fields.Nested(view_output1))   # ties为一个列表
}
class ErhouseResource(Resource):
    def get(self):
        print("请求数据成功***********")
        a = request.args.get("pageCode")
        b = request.args.get("limitNum")
        a = int(a)
        b = int(b)
        ties = TSource.query.all()[a:b]
        data = {
            "code": "666",
            "msg": '查询成功',
            "data": ties
        }
        return marshal(data, view_output)

