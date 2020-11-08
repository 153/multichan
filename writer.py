import os
import time
from flask import Blueprint
from flask import request
import pagemaker as p

writer = Blueprint("writer", __name__)
tdir = "threads"
with open("templ/newt.t", "r") as newtt:
    newtt = newtt.read()

def mk_op(title="", tags=["random"], author="Anonymous", msg=""):
    msg = msg.replace("<", "&lt;").replace("&", "&amp;")    
    msg = msg.replace("\n","<br>").replace("\r","")
    if not title.strip() or not msg.strip():
        return "Please write a message to create a new conversation."
    if not author:
        author = "Anonymous"
    # author, tstamp, msg
    tnow = str(int(time.time()))

    t_loc = ["local", tnow]
    b_pat = f"./{tdir}/local/"
    t_pat = b_pat + tnow + "/"
    os.mkdir(t_pat)

    head = [title, ", ".join(tags)]
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

def rep_t(board, thread, now, author, msg):
    # open board/thread/local
    # append post json
    # update list.txt
    # update board/list
    tdir = f"./threads/{board}/{thread}/"
    tnow = now
    msg = msg.replace("<", "&lt;").replace("&", "&amp;")    
    msg = msg.replace("\n","<br>").replace("\r","")
    rline = "<>".join([tnow, author, msg]) + "\n"
    with open(tdir + "local.txt", "a") as thread:
        thread.write(rline)
    with open(tdir + "list.txt", "a") as tlist:
        tlist.write(f"local {tnow}\n")

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
    print(newl)
    
#@writer.route('/create', methods=['POST', 'GET'])
@writer.route('/create/', methods=['POST', 'GET'])
def new_thread():
    if request.method == 'POST':
        if request.form['sub'] == "Create chat":
            mk_op(title=request.form['title'],
                  tags=["random"],
                  author=request.form['author'],
                  msg=request.form['message'])
            return "<center><h1>" \
                + "Posting thread.....<p>" \
                + "<a href='/threads/'>(back)</a></h1></center>"
        
    return p.mk(newtt)
