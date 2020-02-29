from flask import jsonify

from tools.cache_ import get_head_url, save_head_url, add_token
from tools.oss_ import get_oss_img_url
from tools.token_ import gen_token

def y_login(user,user_id):#登录成功后的信息
    token = gen_token(user_id)  # 生成token
    add_token(token, user_id)  # 存入缓存
    head_url = ''
    if user.Avatar_path:
        head_url = get_head_url(user.Avatar_path)  # 从缓存中取头像
        if not head_url:
            head_url = get_oss_img_url(user.Avatar_path)  # 从云服务端取
            save_head_url(user.Avatar_path, head_url)  # 保存在redis
    resp = jsonify({
        'state': 0,
        'msg': '登录成功',
        'token': token,
        'head': head_url
    })
    # 设置响应对象的cookie,
    resp.set_cookie('token', token)
    resp.set_cookie('head', head_url)
    return resp
