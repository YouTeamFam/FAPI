#!/usr/bin/python3
# coding: utf-8
from redis import Redis

rd = Redis('120.27.10.187', port=6378, db=3, decode_responses=True)

def save_code(phone, code):
    rd.set(phone, code, ex=120)  # 两分钟有效时间


def get_code(phone):#根据电话查验证码
    return rd.get(phone)


def add_token(token, user_id):#添加token
    rd.set(token, user_id, ex=3600 * 24 * 7)  # 一周的有效时长


def get_user_id(token):#根据token获取用户id
    # API接口操作时，需要通过接口中token参数获取登录的用户信息
    return rd.get(token)

# ------用户头像的缓存-----
def save_head_url(key, url):
    rd.set(key, url, ex=3600 * 7 * 24)#存入两周


def get_head_url(key):
    return rd.get(key)