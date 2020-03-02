import os
import re
from datetime import datetime

from flask import Blueprint
from sqlalchemy import or_

from apiapp.models import *
from tools.cache_ import *
from tools.code_ import *
from tools.login_ import y_login
from tools.md5_ import hash_encode
from tools.oss_ import get_oss_img_url, upload_head
from tools.settings import TEMP_DIR
from tools.token_ import *
from tools.val_data import *

userblue = Blueprint('userblue',__name__)

@userblue.route('/code/',methods=["GET"])
def get_code():#获取验证码的接口
    phone = request.args.get('phone')
    if phone:
        pattern = '[1][0-9]{10}$'
        if re.match(pattern,phone):#验证手机号格式是否正确
            send_code(phone)#阿里云验证码服务
            return jsonify({
                'state':0,
                'msg':'验证码已经发送'
            })
        else:
            return jsonify({
                'state':2,
                'msg':'手机格式不正确'
            })
    return jsonify({
        'state':1,
        'msg':'手机号不能为空'
    })

@userblue.route('/fdregister/',methods=["POST"])
def fdregister():#房东注册
    resp = validate_json()#判断是否提供了json数据
    if resp:return resp#如果resp有数据，说明没有提供json数据
    resp = validate_params('name','sex','phone','username','pwd','code')#验证提供数据的完整性
    if resp:return resp
    data = request.get_json()#获取接受的数据
    if not valid_code(data['phone'],data['code']):#验证短信验证码和手机号
        return jsonify({
            'state':2,
            'msg':'验证码错误，请重新输入正确的验证码,2分钟后重新获取'
        })
    pwd = hash_encode(data['pwd'])#密码加密
    fuser=TLandlord(l_name=data['name'],sex=data['sex'],phone=data['phone'],l_uname=data['username'],
                   l_pwd=pwd,regi_date=datetime.now(),last_date=datetime.now(),status=1,sou_num=0)

    db.session.add(fuser)
    db.session.commit()

    token = gen_token(fuser.ld_id)#生成token
    add_token(token,fuser.ld_id)#以key,value的形式存入redis

    return jsonify({
        'state':0,
        'msg':'注册并登录成功',
        'token':token
    })

@userblue.route('/login/',methods=['POST'])#手机登录接口
def login():
    resp = validate_json()
    if resp: return resp
    resp = validate_params('type','pwd','username')
    if resp:return resp
    data = request.get_json()
    pwd = hash_encode(data['pwd'])
    if data['type']=='房东':
        user = TLandlord.query.filter(or_(TLandlord.phone==data['username'],TLandlord.l_uname==data['username']),TLandlord.l_pwd==pwd).first()
        if not user:
            return jsonify({
                'state':0,
                'msg':'口令错误了'
            })
        return y_login(user,user.ld_id)
    elif data['type']=='经纪人':
        user = TBroker.query.filter(or_(TBroker.phone==data['username'],TBroker.b_name==data['username']), TBroker.b_pwd==pwd).first()
        if not user:
            return jsonify({
                'state': 0,
                'msg': '口令错误了'
            })
        return y_login(user,user.broker_id)
    elif data['type']=='用户':
        user = TUser.query.filter(or_(TUser.phone==data['phone'],TUser.u_name==data['username']), TUser.u_pwd==pwd).first()
        if not user:
            return jsonify({
                'state': 3,
                'msg': '口令错误了'
            })
        return y_login(user, user.user_id)

@userblue.route('/gfdpwd/',methods=["POST"])#房东修改密码
def gpwd():#修改密码
    resp = validate_json()
    if resp:return resp
    resp=validate_params('newpwd','pwd')
    if resp:return resp
    data = request.get_json()
    newpwd = hash_encode(data['newpwd'])
    pwd = hash_encode(data['pwd'])
    token = request.cookies.get('token')#获取token
    user_id = get_user_id(token)#缓存中获取用户id
    if not user_id:
        return jsonify({
            'state':3,
            'msg':'登录过期，请重新登录'
        })
    user = TLandlord.query.get(user_id)#通过用户id查找用户
    if user.l_pwd==pwd:
        user.l_pwd=newpwd
        user.last_date=datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'state':0,
            'msg':'修改成功'
        })
    return jsonify({
        'state':4,
        'msg':'原密码错误'
    })

@userblue.route('/uphead/',methods=["POST"])#房东上传图像
def uphead():
    load_file = request.files.get('head') #获取上传的图片
    token = request.cookies.get('token')#获取传过来的token
    user_id = get_user_id(token)
    filename=load_file.filename#获取上传文件的名字
    file_path = os.path.join(TEMP_DIR,filename)#图片临时存放的路径
    load_file.save(file_path)#保存文件到临时文件中

    #将临时文件上传到oss服务器忠，并获取到缩小后的图片url
    head_url = upload_head(user_id,filename,file_path)

    #header_url保存到用户表忠
    user = TLandlord.query.get(user_id)
    user.Avatar_path='{}-{}'.format(user_id,filename) #存储在oss商的key对象
    db.session.add(user)
    db.session.commit()

    #讲头像存入redis中
    save_head_url(user.Avatar_path,head_url)

    #删除临时文件
    os.remove(file_path)

    return jsonify({
        'state':0,
        'msg':'上传成功',
        'head':head_url
    })

