# -*- coding: utf-8 -*-

"""
加解密工具
"""

import base64
from Crypto.Cipher import AES


def aes_decode(text):
    enc = base64.urlsafe_b64decode(text)
    key = "MFwwDQYJKoZIhvcA"
    iv = key.decode('utf-8')
    key = key.decode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = cipher.decrypt(enc)
    return str(dec[0:-ord(dec[-1])].decode('utf-8'))
