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
    page = ""
    hpw = bytes(pw, "utf-8")
    hashed = hash(hpw)
    if hashed != s.phash:
        return "password?"
    cook = f"""<meta http-equiv="set-cookie" content="p={pw}">\n"""
    page += "<pre>"
    page += """* <a href="#log">log</a>
* <a href="#ips">ips</a>
* <a href="#delete">delete</a>
* <a href="#bans">bans</a>
* <a href="#friends">friends</a>
* tags
* threads
* an example thread
"""
    # Show the comment / thread log
    page += "<h1 id='log'>#log</h1>"
    page += "site   | thread | reply | ip\n"  
    with open("../0chan.vip/log.txt", "r") as log:
        log = log.read().splitlines()[::-1]
    for n, x in enumerate(log):
        x = x.split(" ")
        x[-1] = ".".join(x[-1].split(".")[:2])
        log[n] = " ".join(x)
    page += "\n".join(log)
    
    # Show the trash posts
    page += "</pre><hr><h1 id='delete'>#delete</h1><pre>"
    with open("../0chan.vip/delete.txt", "r") as delete:
        delete = delete.read().splitlines()[::-1]
        page += "\n".join(delete)

    page += "</pre><hr><h1 id='ips'>#ips</h1><pre>"
    with open("../0chan.vip/ips.txt", "r") as ips:
        ips = ips.read()
    page += "time     | ip       | captcha | approved time\n"
    page += ips
    # Show the bans
    page += "</pre><hr><h1 id='bans'>#bans</h1><pre>"
    with open("../0chan.vip/bans.txt", "r") as bans:
        bans = bans.read()
    page += bans
    
    # Show friends
    page += "</pre><hr><h1 id='friends'>#friends</h1><pre>"
    with open("../0chan.vip/threads/friends.txt", "r") as friends:
        friends = friends.read()
    page += friends
    
    page += "</pre>"
    return p.mk(page)



if __name__ == "__main__":
    print(hash(s.password))
