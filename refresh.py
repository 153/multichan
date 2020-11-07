import os
import settings as s
import utils as u

arc = s.archive

def ldsing(board, thread, sub):
    error = ["list", "head"]
    if sub in error:
        return
    tdir = "/".join(["./threads", board, thread])
    tf = tdir + "/" + sub + ".txt"
    with open(tf, "r") as tf:
        tf = tf.read().splitlines()
    tf = [x.split("<>")[0] for x in tf]
    return tf

def mkthread(board, thread):
    tdir = "./threads/" + board + "/" + thread
    reps = os.listdir(tdir)
    reps = [r for r in reps if r.split(".")[0] in s.friends.keys()]
    reps = [r.split(".")[0] for r in reps]
    reps = [r for r in reps if len(r.strip())]
    threads = {}
    posts = []        
    for r in reps:
        threads[r] = ldsing(board, thread, r)
    for r in threads:
        for p in threads[r]:
            posts.append([r, p])
    posts = sorted(posts, key=lambda x: x[1])
    posts = [" ".join(p) for p in posts]
    posts = "\n".join(posts) + "\n"
    lf = tdir + "/list.txt"
    with open(lf, "w") as lf:
        lf.write(posts)

def addthread(board, thread):
    bpath = "/".join(["./threads", board, "list.txt"])
    tpath = "/".join(["./threads", board, thread])
    tlist = tpath + "list.txt"
    thead = tpath + "head.txt"
    with open(path, "r") as ind:
        ind = ind.read().splitlines()
    threads = [x.split(" ")[0] for x in ind]
    
def ldboard(board, write=0):
    # Generate new board index based on existing thread indexes.
    meta = ["head.txt", "list.txt"]
    tdir = "./threads/" + board
    indpath = "/".join([tdir, meta[1]])
    threads = [x.path for x in os.scandir(tdir) if x.is_dir()]
    bind = [] # first, last, local, total, title
    for thread in threads:
        info = "/".join([thread, meta[0]])
        replies = "/".join([thread, meta[1]])
        with open(info, "r") as info:
            info = info.read().splitlines()[0]
        with open(replies, "r") as replies:
            replies = replies.read().splitlines()
        replies = [r.split(" ") for r in replies]
        breps = [r[0] for r in replies]
        tline = [replies[0][1], replies[-1][1],
                 str(breps.count("local")), str(len(replies)),
                 info]
        bind.append(tline)
    bind.sort(key= lambda x: x[1], reverse=1)
    if not write:
        return bind
    bind = "\n".join([" ".join(t) for t in bind])
    with open(indpath, "w") as ind:
        ind.write(bind)

def mkboard(board):
    tdir = "./threads/" + board
    threads = [x.name for x in os.scandir(tdir) if x.is_dir()]
    for thread in threads:
        mkthread(board, thread)
    ldboard(board, 1)

def pullboard(board):
    f = s.friends
    fn = arc + board + ".new"
    old = arc + board 
    if not board in f:
        return
    url = "/".join([f[board], "raw", "local"])
    indurl = url + "/list.txt"
    newp = [x.split(" ") for x in
           u.wget(indurl, fn).splitlines()
           if x.strip()]
    with open(old, "r") as oldp:
        oldp = [x.split(" ") for x in
               oldp.read().splitlines()
               if x.strip()]
    diff = [x[0] for x in newp if x not in oldp]
    if not diff:
        return
    print(diff)
    for thread in diff:
        turl = "/".join([url, thread])
        path = "/".join(["./threads", board, thread])
        lurl = turl + "/local.txt"
        hurl = turl + "/head.txt"
        lfn = path + "/" + board + ".txt"
        hfn = path + "/head.txt"
        if not os.path.isdir(path):
            os.mkdir(path)
        u.wget(lurl, lfn)
        u.wget(hurl, hfn)
        mkthread(board, thread)
    mkboard(board)
    os.rename(fn, old)

# pullboard("00chan")
#print(ldboard("local"))
#mkboard("local")
#ldboard("local", 1)  
#ldboard("00chan")

# mkthread("local", "1602486291")
# print( "=" * 20)
# threads/00chan/1602225514
# mkthread("00chan", "1602225514")
