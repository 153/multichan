import json
import os
import random
import string
import time
import settings as s
import pagemaker as pm
from captcha.image import ImageCaptcha
from flask import Blueprint
from flask import request

whitelist = Blueprint("whitelist", __name__)
image = ImageCaptcha(fonts=['droid.ttf'])
conf = s.log
klen = 4
tnow = int(time.time())

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def randstr(length):
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

def addlog(ip, ig=0):
    log = ldlog()
    if ip not in log or ig:
        entry = genkey(ip)
        log[ip] = entry
        fi = "\n".join([" ".join(log[x]) for x in log])
        with open(conf, "w") as iplog:
            iplog.write(fi)
    return log

def approve(ip=0, key=""):
    if not ip:
        ip = get_ip()
    now = str(int(time.time()))
    log = ldlog()
    if ip in log:
        if len(log[ip]) == 3:
            if log[ip][2] != key:
                return False
            log[ip].append(now)
            newl = [" ".join(log[k]) for k in log]
            with open(conf, "w") as log:
                log.write("\n".join(newl))
            return True
        else:
            return True
    return False
        

@whitelist.route('/captcha/')
def show_captcha():
    ip = get_ip()
    mylog = addlog(ip)
    logtxt = json.dumps(mylog)
    html = pm.html("captcha").format(mylog[ip][1])
    return pm.mk(html)

@whitelist.route('/captcha/refresh')
def refresh():
    ip = get_ip()
    mylog = addlog(ip, 1)
    return "<meta http-equiv='refresh' content='0;URL=/captcha'>"

@whitelist.route('/captcha/check', methods=['POST', 'GET'])
def check():
    key = request.args.get('key')    
    ip = get_ip()
    log = ldlog()
    out = approve(ip, key)
    out = json.dumps(out)
    if out == "false":
        out = "You have filled the captcha incorrectly."
        out += "<p>Please <a href='/captcha'>solve the captcha.</a>"
        out += "<meta http-equiv='refresh' content='4;URL=/captcha'>"
    if out == "true":
        out = "You filled out the captcha correctly!"
        out += "<p>Please <a href='/rules'>review the rules</a> before posting."
        out += "<meta http-equiv='refresh' content='4;URL=/'>"

    return out
