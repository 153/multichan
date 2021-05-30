from flask import Blueprint
import viewer as v
import tags as t
import pagemaker as p
import settings as s
import tripcode as tr
import whitelist
import time

boards = Blueprint("boards", __name__)
index_p = "./boards/list.txt"

local_b = []
with open(index_p, "r") as index:
    index = index.read().splitlines()
index = [i.split(" ") for i in index]
for i in index:
    if i[0] == "local":
        local_b.append(i)
    
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
        if int(entry[1][0]) == 0: # hidden
            to_hide.append(entry[0])
        elif int(entry[1][0]) == 2: # sticky
            to_sticky.append(entry[0])
        elif int(entry[1][0]) == 3: # sage
            to_sage.append(entry[0])
        else:
            normal.append(entry[0])
                
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
    boards = local_b
    template = "<li><a href='/b/{1}'>{1}</a> (managed by <b><code>{2}</code></b>)"
    page = """<h1>User Boards</h1><div class="info">
Boards are a work in progress system that will allow user-managed 
communities to exist within the Multichannel network.
</div><p>"""
    page += "<div><ul>" + "\n".join([template.format(*i) for i in boards]) + "</ul></div>"
    return p.mk(page)

@boards.route('/b/<board>/')
@boards.route('/b/<board>/list')
def browse(board):
    info = f"./boards/{board}/info.txt"
    page = ["<div>"]
    page.append(f"<a href='/b'>[back]</a>")
    page.append(f"<h1>/{board}/</h1>")
    with open(info, "r") as about:
        about = about.read()
    page.append(about)
    page.append("<hr>")
    page.append(f"<a href='/create/{board}'>Create a new thread on /{board}/</a>")
    page.append("<hr><ul>")
    threads = board_index(board)
#    threads = "\n".join(threads)
    page += threads
    page.append("</ul>")
    print(page)
    page = "\n".join([n for n in page if (len(n) != 2)])
    return p.mk(page)

@boards.route('/b/<board>/<key>')
def mod_thread(board, key):
    new_local = []
    for L in local_b:
        if tr.sec(key) == L[2]:
            if L[0] == "local" and L[1] == board:
                new_local.append(L)
    if not len(new_local):
        return "0"
    return "1"

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
    # 
    datetime = "%a, %b %d, %Y, @ %I%p"
    tindex = load_thread(board, host, thread) # [[host, time, author, comment]]
    tindex = [[x[0], time.strftime(datetime, time.localtime(int(x[1]))),
               *x[2:]] for x in tindex]
    head = f"./threads/{host}/{thread}/head.txt"
    with open(head, "r") as head:
        head = head.read().splitlines()[0]
    page = []
    page.append(f"{s.name} <a href='/b/{board}'>/{board}/</a>")
    page.append(f"<h2>{head}</h2>")
    cnt = {}
    for t in tindex:
        if t[0] not in cnt:
            cnt[t[0]] = 0
        cnt[t[0]] += 1
        t = " ".join(["<div> >>" + "/".join([s.friends[t[0]], str(cnt[t[0]]) ]),
                      "at", t[1] + ",", t[2], "wrote...<p>",
                      t[3], "<hr>"])
        page.append(t)
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
