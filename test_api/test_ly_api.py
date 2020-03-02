#!/usr/bin/python3
# coding: utf-8

import requests

from unittest import TestCase

HOST = 'localhost'
PORT = 5000

base_url = f'http://{HOST}:{PORT}'

data = {
    'phone': '15229106938',
    'token': 'b7b103a177a5fa1ceb0cd1713c00e7a6'
}


# class TestUserApi(TestCase):
def test_a_send_code():
    url = base_url + f'/api/code/?phone={data["phone"]}'
    resp = requests.get(url)
    print(resp.json())

def test_b_regist():
    url = base_url + '/jjrapi/jjrregist/'
    # "b_name", "phone", "sex", "b_uname", "b_pwd","company_id","years",'code'
    resp = requests.post(url, json={
        'b_name': '貂蝉',
        'phone': data['phone'],
        'sex': '女',
        'b_uname': 'diaochan',  # 密文要求（前端）：需要使用hash算法
        'b_pwd':'654321',
        'company_id': 1,
        'years': 1,
        'code':"8305"
    })
    print(resp.json())
# test_a_send_code()
# test_b_regist()

#
def jjr_change():
    url = base_url + '/jjrapi/jjr_change/'
    resp = requests.post(url, json={
        'old_pwd': "654321",
        'new_pwd': '123456'
    }, cookies={'token': data['token']})
    resp_data = resp.json()
    print(resp_data)

jjr_change()


def jjr_upload_head():
    url = base_url+"/jjrapi/upload_head/"
    resp = requests.post(url, files={
        'head': ('jr.jpg', open('jr.jpg', 'rb'), 'image/jpg')
    }, cookies={'token': data['token']})

    print(resp.json())
# jjr_upload_head()


def jjr_get_head():
    url = base_url+"/jjrapi/get_head/"
    resp = requests.get(url,cookies={'token': data['token']})

    print(resp.json())
# jjr_get_head()