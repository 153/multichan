import time
from flask import Blueprint, request
import settings as s

atom = Blueprint("atom", __name__)

tstring = "%Y-%m-%dT%H:%M:%S+00:00"

url = s.url
title = s.name
friends = s.friends

feed_temp = """<?xml version="1.0" encoding="utf-8"?>
  <feed xmlns="http://www.w3.org/2005/Atom">
<title>{title}</title>
<author><name>Anonymous</name></author>
<id>{url}</id>
<link rel="self" href="{link}" />
<updated>{published}</updated>
"""

entry_temp = """  <entry>
<title>{title}</title>
<link rel="alternate" href="{url}" />
<id>{url}</id>
<published>{published}</published>
<updated>{published}</updated>
<content type="html">
{content}
</content>
  </entry>"""

# server_to_list   ldglobal()
# site_to_list     ldsite("site")
# tag_to_list      ldtag("tag")
# thread_to_list   ldthread(host, thread)
# list_to_feed     mkatom(title, html-url, atom-url, list)

def unix2atom(unix):
    atom = time.strftime(tstring, time.localtime(int(unix)))
    return atom

def ldsite(site="local"):
    # sitename, unixtime, atomtime, title, comment
    if site not in friends.keys():
        return None
    fn = "./threads/" + site + "/list.txt"
    with open(fn, "r") as index:
        index = index.read().splitlines()
    index = sorted(index)[::-1]
    for n, i in enumerate(index):
        i = i.split(" ")
        fn = "/".join(["./threads", site, i[0], site + ".txt"])
        with open(fn, "r") as op:
            op = op.read().splitlines()
        op = op[0].split("<>")[2]
        i[4] = " ".join(i[4:])
        i[1] = time.strftime(tstring, time.localtime(int(i[0])))
        index[n] = [site, i[0], i[1], i[4], op]
    return index

def ldglobal():
    flist = friends.keys()
    globalindex = [ldsite(f) for f in flist]
    globalindex = [x for y in globalindex for x in y]
    for n, g in enumerate(globalindex):
        globalindex[n][3] = f"[{g[0]}] {g[3]}"
    globalindex.sort(key = lambda x: x[1], reverse=True)
    return globalindex

def ldtag(tag="random"):
    globalindex = ldglobal()
    with open("./threads/tags.txt", "r") as tags:
        tags = tags.read().splitlines()
    tags = [t.split() for t in tags]
    tagdb = {t[0]: t[1:] for t in tags}
    if tag not in tagdb:
        return
    tag = [t.split("-") for t in tagdb[tag]]
    tagindex = [t for t in globalindex if t[:2] in tag]
    return tagindex

def ldthread(host, thread):
    hosts = []
    data = []
    thread_dir = "/".join(["./threads", host, thread])
    index = thread_dir + "/list.txt"
    with open(index, "r") as index:
        index = index.read().splitlines()
    index = [i.split(" ") for i in index]
    hosts = list(set([i[0] for i in index]))
    files = ["/".join([thread_dir, host + ".txt"]) for host in hosts]
    for n, i in enumerate(files):
        with open(i, "r") as slice:
            slice = slice.read().splitlines()
        slice = [[hosts[n], *s.split("<>")] for s in slice]
        data.append(slice)
    data = [x for y in data for x in y][::-1]
    for n, d in enumerate(data):
        data[n][2] = unix2atom(d[1])
        data[n].insert(3, f"Reply from {d[0]}")
    return data

def ldcmts():
    # sitename, unixtime, atomtime, title, comment
    # site thread number ipaddress time<>name<>comment
    if not s.logcomment:
        return ""
    with open(s.log, "r") as log:
        log = log.read().splitlines()[:-20:-1]
    log = [x.split()for x in log]
    results = []
    for x in log:
        # board thread num ip    time author comment
        print(x)
        reply = x[4].split("<>")
        try:
            int(reply[0])
        except:
            continue
        reply[2] += " " + " ".join(x[5:])
        url = x[1] + f"#{s.url}/" + x[2]
        result = [x[0], url, unix2atom(reply[0]),
                  f"Reply to {x[0]}/{x[1]}", reply[2]]
        
        # sitename, unixtime, atomtime, title, comment
        results.append(result)
    return results
    

def mkatom(title, link, atomloc, index):
    feed = {}
    if len(index) < 1:
        return
    feed["title"] = title
    feed["url"] = url + link
    feed["link"] = url + atomloc
    feed["published"] = index[0][2]
    body = []
    for i in index:
        entry = {}
        entry["title"] = i[3]
        entry["url"] = "/".join([url, "threads", i[0], i[1]])
        entry["published"] = i[2]
        entry["content"] = i[4]\
            .replace("<", "&lt;").replace(">", "&gt;")
        body.append(entry_temp.format(**entry))
    head = feed_temp.format(**feed)    
    atom = "\n".join([head, "\n".join(body), "</feed>"])
    return atom
    
@atom.route('/atom/global.atom')
def showglobal():
    threads = ldglobal()
    _title = "Known network @ " + title
    return mkatom(_title, "/threads/",
                  "/atom/global.atom", threads)

@atom.route('/atom/<board>.atom')
def showsite(board):
    threads = ldsite(board)
    _title = " ".join([board, "@", title])
    return mkatom(_title, f"/threads/{board}",
                  "/atom/{board}.atom", threads)

@atom.route('/atom/tag/<tag>.atom')
def showtag(tag):
    threads = ldtag(tag)
    _title = " ".join(["Tag", "#"+tag, "@", title])
    return mkatom(_title, f"/tags/{tag}",
                  "/atom/tag/{tag}.atom", threads)

@atom.route('/atom/<host>/<thread>.atom')
def showthread(host, thread):
    threads = ldthread(host, thread)
    with open("/".join(["./threads", host, thread, "head.txt"]), "r") as head:
        head = head.read().splitlines()
    _title = head[0]
    return mkatom(_title, f"/threads/{host}/{thread}",
                  "/atom/{host}/{thread}.atom", threads)

@atom.route('/atom/log.atom')
def showlog():
    posts = ldcmts()
    _title = "Last 20 comments @ " + title
    return mkatom(_title, "/threads/", "/atom/log.atom", posts)
    

@atom.route('/atom/')
def splash():
    return """<style>a {color:green}</style>
<pre>Generate an ATOM feed of the known network:
  - <a href="/atom/global.atom">/atom/global.atom</a>

Generate an ATOM feed of SITE_NAME (ex: local)
  - <a href="/atom/local.atom">/atom/local.atom</a>
  - /atom/SITE_NAME.atom

Generate an ATOM feed of TAG_NAME (ex: random)
  - /atom/tag/TAG_NAME.atom

Generate an ATOM feed of THREAD from SITE (ex: local/0)
  - <a href="/atom/local/0.atom">/atom/local/0.atom</a>
  - /atom/SITE/THREAD.atom

Generate an ATOM feed of last 20 comments from local site:
  - <a href="/atom/log.atom">/atom/log.atom</a>
 </pre>"""
