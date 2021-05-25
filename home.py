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

@home.route('/stats/')
def counter():    
    with open("./static/counter.txt", "r") as cnt:
        cnt = int(cnt.read().strip())
    with open("./static/counter.txt", "w") as update:
        update.write(str(cnt + 1))
    with open(s.bans, "r") as bans:
        bans = bans.read().splitlines()
    with open(s.delete, "r") as dele:
        dele = dele.read().splitlines()

    with open("./threads/list.txt", "r") as threads:
        threads = threads.read().splitlines()
    with open("./threads/tags.txt", "r") as tags:
        tags = tags.read().splitlines()
    tcnt = str(len(threads))
    lcnt = str(len([t for t in threads if t[:6] == "local "]))
    rcnt = str(sum([int(t.split(" ")[3]) for t in threads]))
    acnt = str(sum([int(t.split(" ")[4]) for t in threads]))
    dcnt = str(len(dele))
    bcnt = str(len(bans))
    tags = str(len(tags))
    atags = str(len(s.tags))

    page = []
    page.append(" ".join([f"You are visitor #{cnt+1}",
                          "to this stats page at", s.url, "<ul>"]))
    page.append(" ".join(["<li>", str(len(s.friends)), "friend servers"]))
    page.append(" ".join(["<li>", atags, "featured tags"]))
    page.append(" ".join(["<li>", tags, "unique tags<p>"]))
    page.append(" ".join(["<li>", lcnt, "local threads"]))                
    page.append(" ".join(["<li>", tcnt, "known threads<p>"]))
    page.append(" ".join(["<li>", rcnt, "local replies"]))
    page.append(" ".join(["<li>", acnt, "total replies<p>"]))
    page.append(" ".join(["<li>", dcnt, "deleted posts"]))
    page.append(" ".join(["<li>", bcnt, "banned addresses"]))
    page.append("</ul>")
    return p.mk("\n".join(page))

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
