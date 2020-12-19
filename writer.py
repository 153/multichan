import os
import time
import re
from flask import Blueprint, request
import refresh
import tags
import whitelist
import tripcode
import settings as s
import pagemaker as p


writer = Blueprint("writer", __name__)
tdir = "threads"
with open("templ/newt.t", "r") as newtt:
    newtt = newtt.read()

def nametrip(name):
    if "#" in name:
        name = name.split("#")[:2]
        if len(name[1]):
            print(name)
            name[1] = tripcode.mk(name[1])
        else:
            name[1] = " none"
        if not len(name[0]):
            name[0] = "Anonymous"
        name = "<b><a> !".join(name) + "</a></b>"
    return name
    
def log(board, thread, post):
    ip = whitelist.get_ip() + "\n"
    line = " ".join([board, thread, post, ip])
    iplog = ""
    with open(s.log, "r") as logger:
        postlog = logger.read()
    postlog += line
    with open(s.log, "w") as logger:    
        logger.write(postlog)        
    
def mk_op(title="", tag="random", author="Anonymous", msg=""):
    title = title[:s._short]
    tag = tag[:s._short]
    msg = msg[:s._long]
    msg = msg.replace("<", "&lt;").replace("&", "&amp;")    
    msg = msg.replace("\n","<br>").replace("\r","")
    if not title.strip() or not msg.strip():
        return "Please write a message to create a new conversation."
    if not author:
        author = "Anonymous"
    author = nametrip(author)
    if len(tag) == 0:
        tag = "random"
    pat = re.compile(r'^[ A-Za-z0-9_-]*$')
    tag = " ".join(list(set(re.findall(r'\w+', tag))))
    # author, tstamp, msg
    tnow = str(int(time.time()))

    t_loc = ["local", tnow]
    b_pat = f"./{tdir}/local/"
    t_pat = b_pat + tnow + "/"
    os.mkdir(t_pat)

    head = [title, tag]
    files = {"head": t_pat + "head.txt",
             "list": t_pat + "list.txt",
             "op": t_pat + "local.txt"}

    with open(files["head"], "w") as headf:
        headf.write("\n".join(head))
    if os.path.isfile(files["list"]):
        with open(files["list"], "r") as listf:
            li = li.read().splitlines()
    else:
        li = []
    li.append(f"local {tnow}")
    li = "\n".join(li) + "\n"
    with open(files["list"], "w") as listf:
        listf.write(li)
    with open(files["op"], "w") as opf:
        opf.write("<>".join([tnow, author, msg]) + "\n")
    with open(b_pat + "list.txt", "r") as bind:
        bind = bind.read().splitlines()
    upd = [t_loc[1], t_loc[1], "1 1", title]
    bindex = [b for b in bind if len(b) > 4]
    bindex.append(" ".join(upd))
    bindex = "\n".join(bindex)
    with open(b_pat + "list.txt", "w") as bind:
        bind.write(bindex)
    log("local", tnow, "1")

    refresh.mksite()
    tags.mkboard("local")
    tags.mksite()

def rep_t(board, thread, now, author, msg):
    # open board/thread/local
    # append post json
    # update list.txt
    # update board/list
    if not author:
        author = "Anonymous"
    else:
        author = nametrip(author)
    msg = msg[:s._long]
    tdir = f"./threads/{board}/{thread}/"
    tnow = now
    msg = msg.replace("<", "&lt;").replace("&", "&amp;")    
    msg = msg.replace("\n","<br>").replace("\r","")
    rline = "<>".join([tnow, author, msg]) + "\n"
    cnt = 0
    with open(tdir + "local.txt", "a") as t:
        t.write(rline)
    with open(tdir + "local.txt", "r") as t:
        t = t.read().splitlines()
        cnt = len(t)
    with open(tdir + "list.txt", "a") as tlist:
        tlist.write(f"local {tnow}\n")
    log(board, thread, str(cnt))

def update_board(board, thread, now, wr=1):
    tpath = f"./threads/{board}/list.txt"
    with open(tpath, "r") as tf:
        tf = tf.read().splitlines()
    tnum = thread
    tf = [t.split(" ") for t in tf]
    tfd = {t[0]: t[1:] for t in tf}
    tfd[tnum][0] = str(now)
    tfd[tnum][1] = str(int(tfd[tnum][1]) +1) # local 
    tfd[tnum][2] = str(int(tfd[tnum][2]) +1) # total
    newl = []
    for t in tfd:
        newl.append([t, *tfd[t]])
    newl.sort(key=lambda x:x[1], reverse=True)
    newl = "\n".join([" ".join(t) for t in newl])
    if wr:
        with open(tpath, "w") as tpath:
            tpath.write(newl)
        refresh.mksite()
    
    
#@writer.route('/create', methods=['POST', 'GET'])
@writer.route('/create/', methods=['POST', 'GET'])
def new_thread():
    if request.method == 'POST':
        if not whitelist.approve():
                return "You need to solve <a href='/captcha/'>the " \
                            + "captcha</a> before you can post."
        if request.form['sub'] == "Create chat":
            mk_op(title=request.form['title'],
                  tag=request.form['tag'],
                  author=request.form['author'],
                  msg=request.form['message'])
            return "<center><h1>" \
                + "Posting thread.....<p>" \
                + "<a href='/threads/'>(back)</a></h1></center>"
        
    return p.mk(newtt)
