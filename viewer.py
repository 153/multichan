import os
import time
import re
from flask import Blueprint
from flask import request
import utils as u
import settings as s
import pagemaker as p
import writer
import whitelist

viewer = Blueprint("viewer", __name__)
friends = s.friends

with open("templ/post.t", "r") as postt:
    postt = postt.read()
with open("templ/newr.t", "r") as newr:
    newr = newr.read()
with open("templ/thread.t", "r") as threadt:
    threadt = threadt.read()    

def hostlist(li=0):
    hosts = [x.path.split("/")[2]for x
              in os.scandir("./threads/") if x.is_dir()]
    if li == 1:
        return hosts
    hosts2 = hosts
    hosts.remove("local")
    hosts.insert(0, "local")
    hosts =[]
    for x in hosts2:
        hosts.append(f"\n<a href='/threads/{x}'>{x}</a>")
    hosts.insert(0, "\n<a href='/threads/'>Global</a>")
    hosts = "\nSites: " + " \n&diams; ".join(hosts)
    hosts = "<header style='text-align: right'>" + hosts + "\n</header>"
    return hosts

def tlist(host=''):
    linkf = "<td><a href='{0}'>{1}</a><td>{2}"
    linkl = []
    if not host: 
        all_index()
    if host not in s.friends:
        all_index()
#    if host and host in s.friends:
    with open(f"./threads/{host}/list.txt", "r") as toplist:
        toplist = toplist.read().splitlines()
    for t in toplist:
        t = t.split(" ")
        t[4] = " ".join(t[4:])
        t[0] = f"/threads/{host}/{t[0]}/"
        linkl.append(linkf.format(t[0], t[4], t[3]))
    return linkl

def all_index():
    linkf = "<td>{3} <td><a href='{0}'>{1}</a><td> {2} "
    linkl = []
    blist = hostlist(1)
    toplist = []
    for b in blist:
        with open(f"./threads/{b}/list.txt", "r") as t:
            t = t.read().splitlines()
        toplist.append([" ".join([x, b]) for x in t])
    toplist = [y for x in toplist for y in x]
    toplist = [x.split(" ") for x in toplist]
    toplist.sort(key=lambda x:x[1], reverse=1)
    toplist = [" ".join(x) for x in toplist]
    for t in toplist:
        t = t.split(" ")
        t[4] = " ".join(t[4:-1])
        t[0] = f"/threads/{t[-1]}/{t[0]}/"
        if t[-1] == "local":
            pass
        else:
            t[-1] = f"{t[-1]}"
        linkl.append(linkf.format(t[0], t[4], t[3], t[-1]))
    return linkl        

@viewer.route('/threads/')
def view_all():
    tops = all_index()
    tops[0] = f"<header><hr>({len(tops)} discussions) &diams; " \
        + "<a href='/create'>Add new</a></header>" \
        + "<h1>All Sites</h1><table>" \
        + "<tr><th>origin<th>title<th>replies" \
        + "<tr>" + tops[0]
    page = p.mk(hostlist() + "<tr>".join(tops) + "</table>")
    return page

@viewer.route('/threads/<host>/')
def view(host):
    # tlist() takes host input
    if host and host in s.friends:
        url = s.friends[host]
        tops = tlist(host)
        tops[0] = f"<header>({len(tops)} discussions) &diams; " \
        + "<a href='/create'>Add new</a> &diams; " \
        + f"from <a href='{url}'>{url}</a></header>" \
        + f"<h1>{host}</h1><table>" \
        + "<tr><th>title<th>replies" \
        + "<tr>" + tops[0]        
    else:
        tops = tlist()
        tops[0] = "<h1>All Sites</h1><ol><li>" + tops[0]
    if host == "sageru":
        tops[0] = u.bees + tops[0]
    tops[0] = hostlist() + tops[0]
    return p.mk("<tr>".join(tops) + "</table>\n")

#@viewer.route('/threads/<host>/<thread>/')
def view_t(host, thread):
    lock = 0
    tpath = f"./threads/{host}/{thread}/"
    if os.path.isfile(tpath+"lock"):
        lock = 1
    tinfo = {"title":"", "source":"", "tags":"", "messages":""}
    # Get the list of thread replies and the thread title. 
    with open(tpath + "list.txt", "r") as tind:
        thr = [t.split(" ") for t in tind.read().splitlines()]
    with open(tpath + "head.txt", "r") as meta:
        meta = meta.read().splitlines()
    tlink = "<a href='/tags/{0}/'>#{0}</a>"
    meta[1] = meta[1].split(" ")
    meta[1] = " ".join([tlink.format(m) for m in meta[1]])
    tinfo["tags"] = meta[1]
#    meta[1] = "tags: " + meta[1]
    
    # Load the replies.
    hosts = set([t[0] for t in thr])
    tdb = {}
    for b in hosts:
        bfn = tpath + b + ".txt"
        with open(bfn, "r") as bfn:
            bfn = bfn.read().splitlines()
        for n, x in enumerate(bfn):
            x = x.split("<>")
            if s.ihost in x[2]:
                try:
                    x[2] = u.imgur(x[2])
                except:
                    continue
            tdb[x[0]] = [b, *x, n]

    threadp = []
    pnum = 0
    psub = 0
    cnt = {friends[x]: 0 for x in hosts}
    for p in sorted(tdb.keys()):
        p = tdb[p]
        p.append(p[0])
        p[4], p[5] = p[5], p[4]
        aname = friends[p[0]]
        if p[0] == host:
            pnum += 1
            psub = 0
            p[0] = f"<a id='{pnum}' href='#{pnum}' " \
                + f"onclick='quote(\"{pnum}\")'>#{str(pnum)}</a>"
        else:
            psub += 1
            cnt[aname] += 1
            p[0] = ",".join([str(pnum), str(psub)])
            p[0] = f"<a id='{aname}/{cnt[aname]}' name='{p[0]}' href='#{aname}/{cnt[aname]}' " \
                + f"onclick='quote(\"{aname}/{cnt[aname]}\")'>#{p[0]}</a>"
        if p[4] != "local":
            p[4] = f"&#127758; <a href='{friends[p[4]]}'>{p[4]}</a>"
        else:
            p[4] = ""
        p[3] = p[3].split("<br>")
        p[3] = "<br>".join([f"<b class='quote'>{x}</b>"
                          if len(x) and x[0] == ">" else x
                            for x in p[3]])
        p[1] = u.unix2hum(p[1])
        p[3] = p[3].replace("&amp;", "&")
        
        # Set up >>linking
        fquote = {">>" + friends[f]: f for f in friends}
        replies = []
        for f in fquote:
            if f in p[3]:
                p[3] = p[3].split(f)
                for n, x in enumerate(p[3]):
                    if "</" in x:
                        x = x.split("</")[0]
                        if " " in x:
                            x = x.split(" ")[0]
                        replies.append([f, x])
                p[3] = f.join(p[3])
        replies = ["".join(x) for x in replies]
        for r in replies:
            try:
                if "http" in r2:
                    r2 = ">>http://" + r.split("/")[2]
                elif "https" in r2:
                    r2 = ">>https://" + r.split("/")[2]
                r2 = r.replace(r2, ">>" + fquote[r2])
            except:
                r2 = r
            rep = "<a href='#" + r[2:] + "'>" \
                + r2 + "</a>"
            p[3] = p[3].replace(r, rep)

        if re.compile(r'>>[\d]').search(p[3]):
            p[3] = re.sub(r'>>([\d\,]+)([\s]?)<',
                          r'<a href="#\1">&gt;&gt;\1</a><',
                          p[3])

        p = postt.format(*p)
        threadp.append(p)
    tinfo["messages"] = "".join(threadp)
    tinfo["title"] = meta[0]
    if lock:
        tinfo["title"] = "&#x1F512; " + tinfo["title"]
#    threadp.insert(0, f"<h1>{meta[0]}</h1>")
#    threadp[0] += "source: "
    if host != "local":
        tinfo["source"] += "&#127758;"
    tinfo["source"] += "<a href='/threads/{0}/'>{0}</a>".format(host)
    thread = threadt.format(tinfo["title"], tinfo["source"], tinfo["tags"],
                   tinfo["messages"])    
    if host == "sageru":
        thread = u.bees + thread
    return thread

@viewer.route('/threads/<host>/<thread>/', methods=['POST', 'GET'])
def reply_t(host, thread):
    now = str(int(time.time()))
    if request.method == 'POST':
        if request.form['sub'] == "Reply":
            author = request.form["author"] or "Anonymous"
            message = request.form["message"]
            if not message:
                return "please write a message"
            if not whitelist.approve():
                return "please solve <a href='/captcha'>the captcha</a>"
            tpath = "/".join(["./threads", host, thread, "local.txt"])
            flood = whitelist.flood(s.post)
            if flood: return flood            
            writer.rep_t(host, thread, now, author, message)
        writer.update_host(host, thread, now)
        redir = f"/threads/{host}/{thread}"
        return f"<center><h1><a href='{redir}'>View updated thread</a></h1></center>"
    tpage = view_t(host, thread)
    canpost = whitelist.approve()
    lock = 0
    if os.path.isfile(f"./threads/{host}/{thread}/lock"):
        lock = 1
    if not canpost:
        replf = whitelist.show_captcha(1, f"/threads/{host}/{thread}/")
    elif lock:
        replf = "<hr> <div> &#x1F512; Thread has been locked. No more comments are allowed.</div>"
    else:
        replf = newr.format(host, thread)
    tpage += replf
    return p.mk(str(tpage))
