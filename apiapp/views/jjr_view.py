import os
import re
from apiapp.models import *
from flask import Blueprint, request, jsonify
from datetime import datetime
from tools.code_ import *
from tools.token_ import *
from tools.cache_ import *
from tools.md5_ import *
from tools.val_data import *
from tools.settings import *
from tools.oss_ import *
jjrblue = Blueprint('jjrblue',__name__)

@jjrblue.route('/jjrregist/', methods=['POST'])
def jjrregist():
    # 要求JSON数据格式：
    valid_fields = {"b_name", "phone", "sex", "b_uname", "b_pwd","years",'code',"company_id"}
    data = request.get_json()  # 获取上传的json数据
    if data is None:
        return jsonify({
            'state': 4,
            'msg': '必须提供json格式的参数'
        })

    # 验证参数的完整性
    print(set(data.keys()))
    if set(data.keys()) == valid_fields:
        # 验证输入的验证码是否正确
        if not valid_code(data['phone'], data['code']):
            return jsonify({
                'state': 2,
                'msg': '验证码输入错误，请确认输入的验证码'
            })
        if TBroker.query.filter_by(b_uname=data.get('b_name'),b_pwd=hash_encode(data.get('b_pwd'))):
            return jsonify({
                'state': 3,
                'msg': '用户名和密码重复，请重新输入'
            })
        user = TBroker()
        user.b_name = data.get('b_name')
        user.phone = data.get('phone')
        user.sex = data.get('sex')
        user.b_uname = data.get('b_uname')
        b_pwd = data.get('b_pwd')
        b_pwd = hash_encode(b_pwd)
        user.b_pwd = b_pwd
        user.company_id = data.get('company_id')
        user.status = 0
        user.clinch_num = 0
        user.sou_num = 0
        user.years = data.get('years')
        user.regi_date = datetime.now()
        db.session.add(user)
        db.session.commit()

        # 向前端返回信息中，包含一个与用户匹配的token(有效时间为一周)
        # 1. 基于uuid+user_id生成token
        # 2. 将token和user_id保存到缓存（cache_.save_token(token, user_id)）
        # JWT 单点授权登录
        token = gen_token(user.broker_id)
        add_token(token, user.broker_id)
    else:
        return jsonify({
            'state': 1,
            'msg': data.keys(),
        })

    return jsonify({
        'state': 0,
        'msg': '注册并登录成功',
        'token': token
    })


@jjrblue.route('/jjr_change/', methods=['POST'])
def modify_auth():
    resp = validate_json()
    if resp: return resp

    resp = validate_params('old_pwd', 'new_pwd')
    if resp: return resp

    data = request.get_json()

    try:
        token = request.cookies.get('token')
        user_id = cache_.get_user_id(token)
        if not user_id:
            jsonify({
                'state': 3,
                'msg': '登录已期，需要重新登录并获取新的token',
            })

        user = TBroker.query.get(int(user_id))
        old_pwd = data['old_pwd']
        oldpwd = hash_encode(old_pwd)
        new_pwd = data['new_pwd']
        newpwd = hash_encode(new_pwd)
        if user.b_pwd == oldpwd:
            user.b_pwd = newpwd
            user.regi_date = datetime.now()
            db.session.add(user)
            db.session.commit()

            return jsonify({
                'state': 0,
                'msg': '修改成功'
            })
        return jsonify({
            'state': 4,
            'msg': '原口令不正确'
        })
    except:
        pass

    return jsonify({
        'state': 2,
        'msg': 'token已无效，尝试重新登录',
    })

@jjrblue.route('/upload_head/', methods=["POST"])
def jjr_upload_head():
    # 前端上传图片的两种方式（文件对象上传， base64字符串上传）
    # FileStorage:  'content_length', 'content_type', 'filename', 'headers', 'mimetype', 'save',
    upload_file = request.files.get('head')
    token = request.cookies.get('token')  # 1. 从请求参数中获取  2. 从请求头的Cookie中获取

    print(upload_file.filename, upload_file.content_type, upload_file.mimetype)

    user_id = cache_.get_user_id(token)
    file_name = upload_file.filename

    save_file_path = os.path.join(TEMP_DIR, file_name)
    # 保存上传的文件到临时的目录中
    upload_file.save(save_file_path)

    # 将临时的文件上传到oss服务器中， 并获取到缩小后的图片URL
    head_url = upload_head(user_id, file_name, save_file_path)

    # 将head_url保存到用户的表中
    user = TBroker.query.get(user_id)
    user.Avatar_path = f'{user_id}-{file_name}'  # 存储oss上的key对象
    db.session.add(user)
    db.session.commit()

    # 将头像的URL 存到 redis中
    cache_.save_head_url(user.Avatar_path, head_url)

    # 删除临时的文件
    os.remove(save_file_path)

    return jsonify({
        'state': 0,
        'msg': '上传成功',
        'head': head_url
    })


@jjrblue.route('/get_head/', methods=["GET"])
def jjr_get_head():
    token = request.cookies.get('token')  # 1. 从请求参数中获取  2. 从请求头的Cookie中获取

    user_id = cache_.get_user_id(token)

    user = TBroker.query.get(user_id)

    head_url = cache_.get_head_url(user.Avatar_path)
    if not head_url:
        head_url = get_oss_img_url(user.Avatar_path)
        cache_.save_head_url(user.Avatar_path, head_url)

    return jsonify({
        'state': 0,
        'head': head_url
    })




