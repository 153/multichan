from hashlib import sha256
from flask import Blueprint, request
import settings as s
import pagemaker as p

admin = Blueprint("admin", __name__)

def hash(pw=''):
    hash = sha256()
    hash.update(pw)
    return str(hash.hexdigest())

@admin.route('/admin/')
def front():
    return "password needed"

@admin.route('/admin/<pw>')
def login(pw):
    hpw = bytes(pw, "utf-8")
    hashed = hash(hpw)
    if hashed != s.phash:
        return "password?"
    cook = f"""<meta http-equiv="set-cookie" content="p={pw}">\n"""
    return cook + "welcome"


if __name__ == "__main__":
    print(hash(s.password))
