import hashlib

SECRET_KEY = '8)&#$ii(z#mp_m)*tcn6qa(6pxtc3yyx33wn)hp-8_b$^6_chz'
def hash_encode(txt, secret_sign=SECRET_KEY):
    auth_m = hashlib.md5(txt.encode('utf-8'))
    auth_m.update(secret_sign.encode('utf-8'))
    return auth_m.hexdigest()


if __name__ == '__main__':
    print(hash_encode('123456'))