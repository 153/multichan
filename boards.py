from flask import Blueprint
import viewer as v
import tags as t
import pagemaker as p
import settings as s

boards = Blueprint("boards", __name__)
index = "./boards/list.txt"

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
    
    mfile = f"./boards/{board}/mod.txt"
    to_hide = [] # 0
    to_sticky = [] # 2
    to_sage = [] # 3
    
    normal = [] 
    sages = []
    stickies = []
    with open(mfile, "r") as mod:
        mod = mod.read().splitlines()
    for n, m in enumerate(mod):
        entry = m.split(" @ ")
        entry[0] = entry[0].split(" ")
        if int(entry[1][0]) == 0:
            to_hide.append(entry[0])
        elif int(entry[1][0]) == 2:
            to_sticky.append(entry[0])
        elif int(entry[1][0]) == 3:
            to_sage.append(entry[0])
            
    print(mod)
    
    link = "<li> <a href='{0}'>{1}</a> ({2} replies)"
    sticky = "<li> &#128204; <a href='{0}'>{1}</a> ({2} replies)"
    sage = "<li> &#9875; <a href='{0}'>{1}</a> ({2} replies)"
    
    for n, entry in enumerate(info):
        item = [entry[0], entry[1]]
        url = "/".join(["/threads", *item])
        link_data = [url, entry[5], entry[4]]
        if item in to_sticky:
            stickies.append(sticky.format(*link_data))
        elif item in to_sage:
            sages.append(sage.format(*link_data))
        elif item not in to_hide:
            normal.append(link.format(*link_data))

    links = []
    links += stickies
    links += normal
    links += sages
    return links

@boards.route('/b/')
def splash():
    with open(index, "r") as boards:
        boards = boards.read().splitlines()
    boards = [i.split(" ") for i in boards]
    boards = [i for i in boards if i[0] == "local"]
    template = "<li><a href='/b/{1}'>{1}</a> (managed by <b><code>{2}</code></b>)"
    page = """<h1>User Boards</h1><div class="info">
Boards are a work in progress system that will allow user-managed 
communities to exist within the Multichannel network.
</div><p>"""
    page += "<div><ul>" + "\n".join([template.format(*i) for i in boards]) + "</ul></div>"
    return p.mk(page)

@boards.route('/b/<board>/')
def browse(board):
    mod = f"./boards/{board}/mod.txt"    
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
    
    return p.mk("\n".join(page))

def load_thread(board, host, thread):
    board = "meta"
    host = "0chan"
    thread = "0"
    i = [ ["meta", "0chan", "0", "0chan", "5"] ]

#    # host/thread / list.txt -> 0chan, 52chan, kuzlol
#    { "host": [
#        ["name", "reply"],
#        ["name", "reply"]],
#       "host2":[] }

@boards.route('/b/<board>/0')
def front(board):
    with open(f"./threads/{board}/list.txt", "r") as index:
        index = index.read().splitlines()
