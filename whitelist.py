import json
import os
import random
import string
import time
import settings as s
import pagemaker as pm
from flask import Blueprint
from flask import request
from captcha.image import ImageCaptcha

whitelist = Blueprint("whitelist", __name__)
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

def genkey(ip):
    entry = [str(tnow), ip, str(randstr(klen))]
    image.write(entry[2], f'./static/cap/{ip}.png')
    return entry

def addlog(ip):
    log = ldlog()
    if ip not in log:
        entry = genkey(ip)
        log[ip] = entry
        fi = "\n".join([" ".join(log[x]) for x in log])
        print(fi)
        with open(conf, "w") as iplog:
            iplog.write(fi)
#    log = "\n".join([" ".join(log[x]) for x in log])
    return log

@whitelist.route('/captcha/')
def show_captcha():
    ip = get_ip()
#    ip = "127.0.0.1"
    mylog = addlog(ip)
    logtxt = json.dumps(mylog)
    html = pm.html("captcha").format(mylog[ip][1])
    return pm.mk(html)
