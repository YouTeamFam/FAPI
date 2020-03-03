#!/usr/bin/python3
# _*_coding:utf-8_*_
import os
import re
from datetime import datetime
from flask import Blueprint,request,jsonify

#模型
from apiapp.models import *
#短信验证code redis存储
from tools import settings, oss_
from tools.cache_ import *
#阿里云短信服务
from tools.code_ import *
#md5加密
from tools.md5_ import hash_encode
#生成token
from tools.token_ import *
#json完整型验证
from tools.val_data import *


pt_user_blue = Blueprint('pt_user_blue',__name__) #蓝图


@pt_user_blue.route('/usercode/',methods=['GET'])
def get_code():  #验证码接口
    phone = request.args.get('phone')
    if phone:
        phonePattern = '[1][0-9]{10}$'
        if re.match(phonePattern,phone):  #验证手机号是否符合
            send_code(phone)  #阿里云短信服务向手机发送短信
            return jsonify({
                'state': 0,
                'msg': '验证码已经发送'
            })
        else:
            return jsonify({
                'state': 2,
                'msg': '手机格式不正确'
            })
    else:
        return jsonify({
            'state': 1,
            'msg': '手机号不能为空'
        })

@pt_user_blue.route('/userregister/',methods=['POST'])
def user_register():  #用户注册接口
    resp = validate_json()#判断是否提供了json数据
    if resp:return resp#如果resp有数据，说明没有提供json数据
    resp = validate_params('username','pwd','phone','code','sex')  #验证提供数据的完整性
    if resp:return resp
    data = request.get_json()#获取接前端json数据
    if not valid_code(data['phone'],data['code']): #如果短信验证码和手机号在redis查不到则验证码错误
        return jsonify({
            'state':2,
            'msg':'验证码错误，请重新输入正确的验证码,2分钟后重新获取'
        })
    pwd = hash_encode(data['pwd'])     #将密码加密

    new_user = TUser(u_name=data['username'],u_pwd=pwd,
                     phone=data['phone'],sex=data['sex'],
                     regi_date=datetime.now(),last_date=datetime.now(),
                     status=1,balance=0)

    db.session.add(new_user)
    db.session.commit()

    token = gen_token(new_user.user_id)  #将用户id传入，生成token
    add_token(token, new_user.user_id)  # 以key,value的形式存入redis 有效天数一周

    return jsonify({    #将token给前端一份
        'state':0,
        'msg':'注册并登录成功',
        'token':token
    })


@pt_user_blue.route('/userpwd/',methods=['POST'])
def alter_user_pwd(): #修改密码接口
    resp = validate_json()#判断是否提供了json数据
    if resp:return resp#如果resp有数据，说明没有提供json数据
    resp = validate_params('new_pwd','old_pwd','token')  #验证提供数据的完整性
    if resp:return resp
    data = request.get_json()  #获取json字符串
    user_id = get_user_id(data['token'])  # 根据token获取用户id
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })

    user = TUser.query.filter_by(user_id=user_id).first() #通过token获取的用户id查用户
    if user.u_pwd == hash_encode(data['old_pwd']):  #判断原密码是否正确
        user.u_pwd = hash_encode(data['new_pwd'])  #修改密码
        user.last_date = datetime.now()  #最后修改时间
        db.session.add(user)
        db.session.commit()  #修改后提交
        return jsonify({
            'state': 0,
            'msg': '修改成功'
        })
    return jsonify({
        'state': 4,
        'msg': '原密码错误'
    })


@pt_user_blue.route('/user_upload_head/',methods=['POST'])
def userUpload_head(): #上传头像接口
    upload_file = request.files.get('head')  #获取头像
    token = request.cookies.get('token')   #从cookie中获取token
    user_id = cache_.get_head_url(token)  # 从redis中获取id

    #查看上传文件属性值
    print(upload_file.filename, upload_file.content_type, upload_file.mimetype)

    file_name = upload_file.filename   #获取图片名称
    save_file_path = os.path.join(settings.TEMP_DIR, file_name)  #图片保存路径
    upload_file.save(save_file_path) #保存
    #图片上传oss服务器中，并获取处理后的图片
    head_url = oss_.upload_head(user_id,file_name,save_file_path)

    #将head_url保存到用户表中的头像位置
    user = TUser.query.filter_by(user_id=user_id).first()
    user.Avatar_path = f'{user_id}-{file_name}'  #作为key存入数据库
    db.session.add(user)
    db.session.commit()  #保存
    # 将头像的URL 存到 redis中
    cache_.save_head_url(user.Avatar_path, head_url)
    # 删除临时的文件
    os.remove(save_file_path)

    return jsonify({
        'state': 0,
        'msg': '上传成功',
        'head': head_url
    })
