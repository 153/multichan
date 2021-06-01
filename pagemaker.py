import os
import settings as s
import utils as u

with open("./html/top.html", "r") as top:
    top = top.read().format(s.name)
with open("./html/bottom.html", "r") as bottom:
    bottom = bottom.read()

if not s.boards:
    top = top.replace('<a href="/b/">boards</a> &clubs;', '')
    
def mk(data=""):
    page = ""

    page += top
    page += data
    page += bottom

    return page

def html(pname):
    path = "./html/" + pname + ".html"
    with open(path, "r") as path:
        path = path.read()
    if not s.boards and pname == "home":
        path = path.replace('<li><a href="/b/">Boards</a>', '')
    return path
