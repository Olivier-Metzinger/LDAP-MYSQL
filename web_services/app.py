#! /usr/bin/python
# -*- coding:utf-8 -*-

import binascii
from flask import request
from flask import Flask
from Crypto.Cipher import AES
from urllib import unquote
import hashlib
import base64
import sys
from phpserialize import unserialize

app = Flask(__name__)

@app.route('/connect', methods=['POST'])
def index():

    pwd = request.args.get("pwd")
    token = request.args.get("token")
    isLoggedIn = token_decrypt(pwd, token)
    if (isLoggedIn['auth']):
         print("YEAH BOY", sys.stdout)
    else:
          print("NOP", sys.stdout)

def token_decrypt(pwd, token):
    key = 'jBRsTvutzj9L18WNVS9y2zsSohcY8X13'
    iv = '3798562014659874'
    encrypted = base64.b64decode(unquote(token).decode('utf8'))

    cipher = AES.new(key,AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(encrypted)

    userData = (unserialize(base64.b64decode(decrypted)))
    hash_object = userData['uuid'] + str(userData['timestamp'])

    result = hashlib.sha512(hash_object.encode()).hexdigest()
    res = pwd == result
    tab = dict()
    tab['auth'] = res
    tab['userData'] = userData
    return tab

def user_exist_ldap:

if __name__ == '__main__':
    app.run(debug=True)
