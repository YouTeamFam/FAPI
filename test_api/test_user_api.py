from unittest import TestCase

import requests

HOST ='localhost'
PORT = 5000
base_url = 'http://{}:{}'.format(HOST,PORT)
data={
    'phone':'15222244240',
    'token':'814d020839f316c2b702108868dc2727',
    'username':'sunjian'
}

class TestUserApi(TestCase):
    def test_a_send_code(self):#获取验证码的接口
        url = base_url+'/api/code/?phone={}'.format(data['phone'])
        resp = requests.get(url)
        print(resp.json())

    def test_b_register(self):
        url = base_url+'/api/fdregister/'
        resp = requests.post(url,json={
            'name':'孙坚',
            'sex':'男',
            'phone':data['phone'],
            'username':'sunjian',
            'pwd':'123456',
            'code':'3926'
        })
        print(resp.json())
    def test_c_login(self):#测试房东登录
        url = base_url+'/api/login/'
        resp = requests.post(url,json={
            'type':'房东',
            'username':data['username'],
            'pwd':'654321'
        })
        print(resp.json())
    def test_d_login(self):#经纪人登录,15229106938,b7b103a177a5fa1ceb0cd1713c00e7a6
        url = base_url+'/api/login/'
        resp = requests.post(url,json={
            'type':'经纪人',
            'phone':'',
            'username':'diaochan',
            'pwd':'123456'
        })
        print(resp.json())
    def test_e_login(self):#用户登录,15229106938,b7b103a177a5fa1ceb0cd1713c00e7a6
        url = base_url+'/api/login/'
        resp = requests.post(url,json={
            'type':'用户',
            'phone':'',
            'username':'wangdan',
            'pwd':'123456'
        })
        print(resp.json())
    def test_e_gfdpwd(self):#修改密码接口
        url = base_url + '/api/gfdpwd/'
        resp = requests.post(url,json={
            'newpwd':'654321',
            'pwd':'123456'
        },cookies={'token':data['token']})
        print(resp.json())
    def test_f_upload_head(self):#上传头像接口
        url = base_url+'/api/uphead/'
        resp = requests.post(url,files={
            'head':('yanzu.jpg',open('yanzu.jpg','rb'),'image/jpg')
        },cookies={'token':data['token']})
        print(resp.json())
