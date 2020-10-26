import os
import settings as s
import utils as u

with open("./html/top.html", "r") as top:
    top = top.read()
with open("./html/bottom.html", "r") as bottom:
    bottom = bottom.read()

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
    return path
