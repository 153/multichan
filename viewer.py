import os
import time
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

def boardlist(li=0):
    boards = [x.path.split("/")[2]for x
              in os.scandir("./threads/") if x.is_dir()]
    if li == 1:
        return boards
    boards2 = boards
    boards =[]
    for x in boards2:
        boards.append(f"\n<a href='/threads/{x}'>{x}</a>")
    boards.insert(0, "\n<a href='/threads/'>Global</a>")
    boards = "\nSites: " + " \n&diams; ".join(boards) + "<hr>"
    boards = "<div style='text-align: right'>" + boards + "\n</div>"
    return boards

def tlist(board=''):
    linkf = "<a href='{0}'>{1}</a> ({2} replies)"
    linkl = []
    if not board: 
        all_index()
    if board not in s.friends:
        all_index()
#    if board and board in s.friends:
    with open(f"./threads/{board}/list.txt", "r") as toplist:
        toplist = toplist.read().splitlines()
    for t in toplist:
        t = t.split(" ")
        t[4] = " ".join(t[4:])
        t[0] = f"/threads/{board}/{t[0]}/"
        linkl.append(linkf.format(t[0], t[4], t[3]))
    return linkl

def all_index():
    linkf = "{3} <a href='{0}'>{1}</a> ({2} replies)"
    linkl = []
    blist = boardlist(1)
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
            t[-1] = "local &emsp;"
        else:
            t[-1] = f"({t[-1]}) :"
        linkl.append(linkf.format(t[0], t[4], t[3], t[-1]))
    return linkl
        

@viewer.route('/threads/')
def view_all():
    tops = all_index()
    tops[0] = f"({len(tops)} discussions) &diams; " \
        + "<a href='/create'>Add new</a><hr>" \
        + "<h1>All Sites</h1><ol><li>" \
        + tops[0]
    page = p.mk(boardlist() + "<li>".join(tops) + "</ol>")
    return page

@viewer.route('/threads/<board>/')
def view(board):
    # tlist() takes board input
    if board and board in s.friends:
        tops = tlist(board)
        tops[0] = f"({len(tops)} discussions) &diams; " \
        + "<a href='/create'>Add new</a><hr>" \
        + f"<h1>{board}</h1><ol><li>" \
        + tops[0]        
    else:
        tops = tlist()
        tops[0] = "<h1>All Sites</h1><ol><li>" + tops[0]
    tops[0] = boardlist() + tops[0]
    return p.mk("<li>".join(tops) + "</ol>")

#@viewer.route('/threads/<board>/<thread>/')
def view_t(board, thread):
    tpath = f"./threads/{board}/{thread}/"
    # Get the list of thread replies and the thread title. 
    with open(tpath + "list.txt", "r") as tind:
        thr = [t.split(" ") for t in tind.read().splitlines()]
    with open(tpath + "head.txt", "r") as thed:
        thed = thed.read().splitlines()[0]
    # Load the replies.
    boards = set([t[0] for t in thr])
    tdb = {}
    for b in boards:
        bfn = tpath + b + ".txt"
        with open(bfn, "r") as bfn:
            bfn = bfn.read().splitlines()
        for x in bfn:
            x = x.split("<>")
            tdb[x[0]] = [b, *x]
    threadp = []
    pnum = 0
    psub = 0
    for p in sorted(tdb.keys()):
        p = tdb[p]
        p.append(p[0])
        if p[0] == board:
            pnum += 1
            psub = 0
            p[0] = str(pnum)
        else:
            psub += 1
            p[0] = ",".join([str(pnum), str(psub)])
        if p[4] != "local":
            p[4] = f"&#127758; <a href='{friends[p[4]]}'>{p[4]}</a>"
        else:
            p[4] = ""
        print(p[3])
        p[3] = p[3].split("<br>")
        print(p[3])
        p[3] = "<br>".join([f"<b class='quote'>{x}</b>"
                          if x[0] == ">" else x for x in p[3]
                            if len(x)])
        p[1] = u.unix2hum(p[1])
        p[3] = p[3].replace("&amp;", "&")
        p = postt.format(*p)
        threadp.append(p)
    threadp.insert(0, f"<h1>{thed}</h1>")
    return "<p>".join(threadp)

@viewer.route('/threads/<board>/<thread>/', methods=['POST', 'GET'])
def reply_t(board, thread):
    now = str(int(time.time()))
    if request.method == 'POST':
        if request.form['sub'] == "Reply":
            message = request.form["message"]
            author = request.form["author"]
            if not author:
                author = "Anonymous"
            if not message:
                return "please write a message"
            if not whitelist.approve():
                return "please solve <a href='/captcha'>the captcha</a>"
            writer.rep_t(board, thread, now,
                         author, request.form["message"])
        writer.update_board(board, thread, now)
        redir = f"/threads/{board}/{thread}"
        return f"<center><h1><a href='{redir}'>View updated thread</a></h1></center>"
    tpage = view_t(board, thread)
    replf = newr.format(board, thread)
    return p.mk(str(tpage + "<hr>" + replf))
