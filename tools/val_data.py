from flask import request, jsonify


def validate_json():#验证是否提供Json格式的数据
    if not request.get_json():
        return jsonify({
            'state': 1,
            'msg': '未提供json格式数据'
        })


def validate_params(*param):#验证参数的完整性
    k1 = ','.join(sorted(list(param)))
    k2 = ','.join(sorted(request.get_json().keys()))
    if not k1 == k2:
        return jsonify({
            "state": 2,
            "msg": "POST请求的json数据参数不完整"
        })