import time
import os
from flask import Blueprint, request
import pagemaker as p
import viewer as v
import tags as t
import settings as s
import tripcode as tr
import whitelist


boards = Blueprint("boards", __name__)
index_p = "./boards/list.txt"
with open(index_p, "r") as index:
    index = index.read().splitlines()
local_b = [i.split(" ") for i in index]

#   /b/
# splash()
#   /b/board/
# browse(board)
#   /b/board/key
# mod_board(board, key)
#   /b/board/host/thread
# show_thread(board, host, thread)
# # board_index(board)
# # load_thread(board, host, thread)

def board_index(board):
    # mod.txt
    # 0 - hide
    # 1 - normal
    # 2 - lock
    # 3 - sticky
    # 4 - lock sticky
    # 5 - permasage
    
    threads = t.tags_threads([board]) # [host, thread]
    with open("./threads/list.txt", "r") as info:
        info = info.read().splitlines() # [host, thread, last, Lrep, Grep, title]
    info = [i.split(" ") for i in info]
    info = [i for i in info if i[:2] in threads]
    info = [[*i[:5], " ".join(i[5:])] for i in info]
    
    mfile = f"./boards/{board}/threads.txt"
    to_hide = [] # 0
    to_sticky = [] # 2
    to_sage = [] # 3

    hidden = []
    normal = [] 
    sages = []
    stickies = []
    
    with open(mfile, "r") as mod:
        mod = mod.read().splitlines()
    for n, m in enumerate(mod):
        entry = m.split(" @ ")
        entry[0] = entry[0].split(" ")
        try:
            if int(entry[1][0]) == 0: # hidden
                to_hide.append(entry[0])
            elif int(entry[1][0]) == 2: # sticky
                to_sticky.append(entry[0])
            elif int(entry[1][0]) == 3: # sage
                to_sage.append(entry[0])
            else:
                normal.append(entry[0])
        except:
            pass
                
    link = "<li> <a href='{0}'>{1}</a> ({2} replies)"
    sticky = "<li> &#128204; <a href='{0}'>{1}</a> ({2} replies)"
    sage = "<li> &#9875; <a href='{0}'>{1}</a> ({2} replies)"
    
    for n, entry in enumerate(info):
        item = [entry[0], entry[1]]
        url = "/".join([f"/b/{board}", *item])
        link_data = [url, entry[5], entry[4]]
        if item in to_sticky:
            stickies.append(sticky.format(*link_data))
        elif item in to_sage:
            sages.append(sage.format(*link_data))
        elif item in to_hide:
            hidden.append(link.format(*link_data))
        else:
            normal.append(link.format(*link_data))

    links = []
    links += stickies
    links += normal
    links += sages
    return links

@boards.route('/b/')
def splash():
    with open(index_p, "r") as index:
        index = index.read().splitlines()
    local_b = [i.split(" ") for i in index]
    boards = local_b
    template = "<li><a href='/b/{0}'>{0}</a> (managed by <b><code>{1}</code></b>)"
    page = """<h1>User Boards</h1><div class="info">
Boards are a work in progress system that will allow user-managed 
communities to exist within the Multichannel network.
</div><p>"""
    page += "<div><ul>" + "\n".join([template.format(*i) for i in boards]) + "</ul></div>"
    return p.mk(page)

@boards.route('/b/<board>/', methods=['POST', 'GET'])
@boards.route('/b/<board>/list')
def browse(board):
    if request.method == 'POST':
        user_key = tr.sec(request.form["key"])
        with open(index_p, "r") as index:
            index = index.read().splitlines()
            local_b = [i.split(" ") for i in index]
        test = [i for i in local_b if (i[0] == board and i[1] == user_key)]
        if not len(test):
            pass
        print(request.form["threads.txt"].strip())
        files = ["info.txt", "hide.txt", "threads.txt"]
        try:
            for f in files:
                path = "./boards/" + board + "/"
                data = request.form[f].strip()
                if f in ["threads.txt", "hide.txt"]:
                    with open(path+f, "w") as out:
                        out.write(data)
                else:
                    with open(path+f, "w") as out:
                        out.write(data)

        except:
            print(board)
            

    info = f"./boards/{board}/info.txt"
    with open(info, "r") as about:
        about = about.read()
    page = ["<div>"]
    page.append(f"<a href='/b'>[back]</a>")
    page.append(f"<h1>/{board}/</h1>")
    page.append(f"<link rel='alternative' type='application/xml' href='/atom/tag/{board}.atom'>")
    page.append(about)
    page.append(f"<p><a href='/create/{board}'>Create a new thread on /{board}/</a>")
    page.append("<hr><ul>")
    threads = board_index(board)
#    threads = "\n".join(threads)
    page += threads
    page.append("</ul>")
    page = "\n".join([n for n in page if (len(n) != 2)])
    return p.mk(page)

def mkboard(board, key):
    key = tr.sec(key)
    path = "./boards/" + board + "/"
    try:
        os.mkdir(path)
    except:
        pass
    with open("./boards/list.txt", "a") as li:
        li.write(f"{board} {key}\n")
    try:
        os.mkdir(path)
    except:
        pass
    files = ["info.txt", "threads.txt", "hide.txt"]
    for f in files:
        _path = path + f
        with open(_path, "w") as fi:
            print(path)
            fi.write("")
    
        

@boards.route('/b/<board>/<key>')
def mod_board(board, key):
    new_local = []
    with open(index_p, "r") as index:
        index = index.read().splitlines()
        local_b = [i.split(" ") for i in index]
    bs = [x[0] for x in local_b]
    if board not in bs:
        mkboard(board, key)
        # abc
        return str([board, key])
    for L in local_b:
        if tr.sec(key) == L[1] and L[0] == board:
            new_local.append(L)
    if not len(new_local):
        return "0"
    page = ["<style>textarea {", "width: 800px; height:120px;}</style>"]
    page.append("<form action='.' method='post'>")
    page.append("<input type='submit' value='Moderate Board'>")
    page.append(f"<input type='hidden' name='board' value='{board}'>")
    page.append(f"<input type='hidden' name='key' value='{key}'>")
    mod = {}
    files = ["info.txt", "threads.txt", "hide.txt"]
    for f in files:
        with open(f"./boards/{board}/{f}", "r") as data:
            data = data.read()
        mod[f] = data + "\n"
    for f in mod:
        page.append(f)
        if f == "threads.txt":
            page[-1] += " // format: host thread @ mode ; 0 hide ; 2 sticky; 3 sage"
        elif f == "hide.txt":
            page[-1] += " // format: host thread host reply# "
        page.append(f"<textarea name='{f}'>{mod[f]}</textarea>")
    return "<pre>" + "\n".join(page) + "</pre>"

def load_thread(board, host, thread):
    # Board view of host:thread 

    # path = [] # [[host, time]]
    posts = {} # {"host": [time, time, time]}
    data = {} # {"host": [[host, time, author, message]] } 
    _thread = [] # [[host, time, author, message]]

    origin = [host, thread] # 0chan, 0
    
    path = f"./threads/{host}/{thread}/"
    hide = f"./boards/{board}/hide.txt"

    with open(path + "list.txt", "r") as path:
        path = path.read().splitlines()
        path = [p.split(" ") for p in path]
    with open(hide, "r") as hide:
        hide = hide.read().splitlines()
        hide = [h.split(" ") for h in hide]
    hide = [h for h in hide if h[:2] == origin]
    print(hide) # posts to filter 
    for p in path:
        # site time
        if p[0] not in posts.keys():
            posts[p[0]] = []
        posts[p[0]].append(p[1])

    # posts[host][reply, reply, reply]
    data = posts.copy() 
    for d in data:
        whereis = f"./threads/{host}/{thread}/{d}.txt"
        with open(whereis, "r") as files:
            files = files.read().splitlines()
            files = [[d, *f.split("<>")] for f in files]
            data[d] = files
    # data[host][rep] = [post, goes, here]
    # {"host": ["host", "time", "author", "message"]}
            
    for h in hide:
        if [host, thread] != [h[0], h[1]]:
            continue
        print(h[2], h[3], "\n")
        print( data[h[2]][int(h[3])-1] )
        data[h[2]][int(h[3])-1] = [data[h[2]][int(h[3])-1][0],
                                 data[h[2]][int(h[3])-1][1],
                                 "<i>deleted</i>",
                                 "<i>message deleted by admin</i>"]
    
    cnt = {} 
    for p in path:
        h = p[0]
        if h not in cnt:
            cnt[h] = 0
        _thread.append(data[h][cnt[h]])
        cnt[h] += 1
    return _thread
    # data["host"][cnt] = ["host", "time", "author", "message"]
    # _thread = list.txt x ["host", "time", "author", "message"]

@boards.route('/b/<board>/<host>/<thread>/')
def show_thread(board, host, thread, methods=['POST', 'GET']):
    datetime = "%a, %b %d, %Y, @ %-I %p"
    test = mod_board(board, host)
    print(board, host, thread)
    print(host, thread)
    tindex = load_thread(board, host, thread) # [[host, time, author, comment]]
    print("!", tindex)
    tindex = [[x[0], time.strftime(datetime, time.localtime(int(x[1]))),
               *x[2:]] for x in tindex]
    head = f"./threads/{host}/{thread}/head.txt"
    with open(head, "r") as head:
        head = head.read().splitlines()[0]
    page = []
    page.append(f"{s.name} <a href='/b/{board}'>/{board}/</a>")
    page.append(f"<h2>{head}</h2>")
    cnt = {}
    render = []
    with open("./templ/post.t", "r") as reply:
        reply = reply.read()
    for t in tindex:
        if t[0] not in cnt:
            cnt[t[0]] = 0
        cnt[t[0]] += 1
        b = [t[0], s.friends[t[0]]]
        ref = f"{b[1]}/{cnt[b[0]]}"
        link = f"<a href='#{ref}' "
        link += f"onclick='quote(\"{ref}\")' id='{ref}'>"
        link += f"&gt;&gt;{b[0]}/{cnt[b[0]]}</a>"
        # 0 reply, # 1 date, #2 name, #3 comment, #4 host
#        t = " ".join(["<div>",
#                      f"<a href='#{b[1]}/{cnt[b[0]]}'>", 
#                      f"&gt;&gt;{b[0]}/{cnt[b[0]]}</a>",
#                      "at", t[1] + ",", t[2], "wrote...<p>",
#                      t[3], "<hr>"])
#        page.append(t)
        # 0 host, # 1 time, #2 author, #3 comment
        
        page.append(reply.format(link, t[1], t[2], t[3], ""))
    canpost = whitelist.approve()
    with open("./templ/newr.t", "r") as newr:
        newr = newr.read().format(host, thread)
    if not canpost:
        replf = whitelist.show_captcha(1, f"/threads/{host}/{thread}/")
    else:
        replf = newr.format(board, thread)
    page.append(replf)
    return p.mk("<br>".join(page))
        
@boards.route('/b/<board>/0')
def front(board):
    with open(f"./threads/{board}/list.txt", "r") as index:
        index = index.read().splitlines()
