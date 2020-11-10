import json
import os
import random
import string
import settings as s
import time
from flask import Blueprint
from flask import request
from captcha.image import ImageCaptcha

secure = Blueprint("secure", __name__)
image = ImageCaptcha(fonts=['droid.ttf'])
conf = s.log
klen = 4
tnow = int(time.time())

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def randstr(length):
#    letters = string.ascii_lowercase
    letters = "bcefgkmopswxz"
    key = "".join(list(random.choice(letters) for i in range(length)))
    return key

def ldlog():
    with open(conf, "r") as log:
        log = log.read().splitlines()
    log = [i.split(" ") for i in log]
    log = {i[1] : i for i in log}
    return log

def addlog(ip):
    entry = [str(tnow), ip, randstr(klen)]
    log = ldlog()
    if ip not in log:
        log[entry[1]] = entry
    for x in log:
        print(" ".join(log[x]))
#    log = "\n".join([" ".join(log[x]) for x in log])
    return log

@secure.route('/captcha/')
def show_captcha():
    ipaddr = get_ip()
#    ipaddr = "123" #get_ip()
    mylog = addlog(ipaddr)
    logtxt = json.dumps(mylog)
    key = mylog[ipaddr][-1]
    image.write(key, f'./static/{ipaddr}.png')
    return f"{ipaddr} <p> <img src='/{ipaddr}.png'><p> {logtxt}"
