import os
from flask import Blueprint
from flask import request
from captcha.image import ImageCaptcha

secure = Blueprint("secure", __name__)

image = ImageCaptcha(fonts=['droid.ttf'])

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@secure.route('/captcha/')
def test():
    ipaddr = get_ip()
#    data = image.generate('he39o')
    image.write('saoa', './static/secure.png')
    
    return f"{ipaddr} <p> <img src='/secure.png'>"
