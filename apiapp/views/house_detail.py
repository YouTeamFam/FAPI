from flask_restful import Resource, marshal_with, fields, marshal
from flask_restful.reqparse import RequestParser
from flask import request
from apiapp.models import TUserPost,TSource

rp1 = RequestParser()
view_output1 = {
    "face": fields.String(attribute="face"),
    "title": fields.String(attribute="title"),
    "region": fields.String(attribute="region"),
    "pub_date": fields.DateTime(attribute="pub_date"),
    "img_url": fields.String(attribute="img_url"),
    "nearby": fields.String(attribute="nearby"),
    "hu_type": fields.String(attribute="hu_type"),
    "comm_name": fields.String(attribute="comm_name"),
    "sum_price": fields.String(attribute="sum_price"),
    "area": fields.String(attribute="area"),
}

view_output = {
    "code": fields.String,
    "msg": fields.String,
    "data": fields.Nested(view_output1)   # ties为一个列表
}
class HouseDetailResource(Resource):
    def get(self):
        print("请求成功*******************")
        source_id = request.args.get("source_id")
        source_id = int(source_id)
        print("*****"*20)
        print(source_id,type(source_id))
        ties = TSource.query.filter_by(source_id=source_id).first()
        print(ties.title)
        data = {
            "code": "666",
            "msg": '查询成功',
            "data": ties
        }
        return marshal(data, view_output)

