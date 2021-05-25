from flask import Blueprint
import pagemaker as p
import settings as s

home = Blueprint("home", __name__)

@home.route('/', strict_slashes=False)
def hello_world():
    return p.mk(p.html("home").format(s.name))

@home.route('/rules')
def rules():
    return p.mk(p.html("rules"))

@home.route('/about')
def about():
    return p.mk(p.html("about"))

@home.route('/stats')
def counter():
    with open("./static/counter.txt", "r") as cnt:
        cnt = int(cnt.read().strip())
    with open("./static/counter.txt", "w") as update:
        update.write(str(cnt + 1))
    return p.mk(" ".join(["You are visitor #", str(cnt+1),
                "to this stats page at", s.url]))

@home.route('/friends')
def friends():
    title = "<h1>Friends of " + s.name
    title += "</h1><h4>" + s.url 
    if s.images:
        title += f"<br>images: <a href='{s.ihost}'>{s.ihost}</a>"
    title += "</h4>"
    title +=  "Friends are other multichan websites that "
    title += "this server downloads threads and comments from."
    flist = []
    fstring = "<li> <a href='{1}'>{0}</a> {1}"
    for f in s.friends:
        flist.append(fstring.format(f, s.friends[f]))
    flist = "<ul>" + "\n".join(flist) + "</ul>"
    page = title + flist
    return p.mk(page)
