#!/usr/bin/python3
#_*_coding:utf-8_*_

from unittest import TestCase

import requests

HOST ='localhost'
PORT = 5000
base_url = 'http://{}:{}'.format(HOST,PORT)
data={
    'phone':'18165143523'
}

class TestUserApi(TestCase):
    def test_a_send_code(self):#获取验证码的接口
        url = base_url+'/api/usercode/?phone={}'.format(data['phone'])
        resp = requests.get(url)
        print(resp.json())

    def test_b_register(self):
        url = base_url+'/api/userregister/'
        resp = requests.post(url,json={
            'username': 'wangdan',
            'pwd': '123456',
            'sex':'女',
            'phone':data['phone'],
            'code':'6518'
        })
        print(resp.json())

    def test_c_alter_pwd(self):
        url = base_url + '/api/userpwd/'
        resp = requests.post(url,json={
            'new_pwd':'654321',
            'old_pwd':'123456',
            'token':'5e86a53f65b22402af86792bc75c43c2'
        })
        print(resp.json())

    def test_d_upload_head(self):
        url = base_url+"/api/user_upload_head/"
        resp = requests.post(url, files={
            'head': ('user1.png', open('user1.png', 'rb'), 'image/jpeg')
        }, cookies={'token':'5e86a53f65b22402af86792bc75c43c2'})

        print(resp.json())