import json
import os
import random
import string
import settings as s
from flask import Blueprint
from flask import request
from captcha.image import ImageCaptcha

secure = Blueprint("secure", __name__)
image = ImageCaptcha(fonts=['droid.ttf'])
conf = s.log
klen = 5

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def randstr(length):
    letters = string.ascii_lowercase
    key = "".join(list(random.choice(letters) for i in range(length)))
    return key

def ldlog():
    with open(conf, "r") as log:
        log = log.read().splitlines()
    log = [i.split(" ") for i in log]
    log = {i[0] : i[1] for i in log}
    return log

def addlog(ip):
    pair = [ip, randstr(klen)]
    log = ldlog()
    if ip not in log:
        log[pair[0]] = pair[1]
    return log

@secure.route('/captcha/')
def test():
    ipaddr = get_ip()
    mylog = addlog(ipaddr)
    logtxt = json.dumps(mylog)
    key = mylog[ipaddr]
    image.write(key, './static/secure.png')
    return f"{ipaddr} <p> <img src='/secure.png'><p> {logtxt}"
