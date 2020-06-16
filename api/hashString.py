import clientServer
import hashlib
import json
from Crypto.Cipher import DES
import base64

def md5Hash(string):
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return string, m.hexdigest()


def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text


def encode(string):
    
    code = string
    key = b'nkust'
    des = DES.new(key, DES.MODE_ECB)
    code = pad(code)
    encrypted_text = base64.b64encode(des.encrypt(code)).decode('UTF-8')
    return encrypted_text


def decode(string):
    try:
        key = b'nkust'
        des = DES.new(key, DES.MODE_ECB)
        b64 = base64.b64decode(string)
        plain_text = des.decrypt(b64).decode("UTF-8").rstrip(' ')
        return plain_text
    except:
        print('wrong')


if __name__ == "__main__":
    #c = clientServer.client(1)
    #c.connect('hashTest', md5Hash('password'))

    testData0 = {
        'account': 'fuck1',
        'password': '可波'
    }

    print(decode(encode(testData0)))
