import os
import tags
import settings as s
import utils as u
import mod

arc = s.archive
friends = s.friends

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
    tdir = "/".join(["./threads", board, thread])
    reps = os.listdir(tdir)
    reps = [r for r in reps if r.split(".")[0] in s.friends.keys()]
    reps = [r.split(".")[0] for r in reps]
    reps = [r for r in reps if len(r.strip())]
    threads = {}
    posts = []        
    for r in reps:
        threads[r] = ldsing(board, thread, r)
    for t in threads:
        for p in threads[t]:
            posts.append([t, p])
    posts = sorted(posts, key=lambda x: x[1])
    posts = [" ".join(p) for p in posts]
    posts = "\n".join(posts) + "\n"
    lf = tdir + "/list.txt"
    with open(lf, "w") as lf:
        lf.write(posts)

def ldboard(board, write=0):
    # Generate new board index based on existing thread indexes.
    meta = ["head.txt", "list.txt"]
    tdir = "/".join(["./threads", board])
    indpath = "/".join([tdir, meta[1]])
    threads = [x.path for x in os.scandir(tdir) if x.is_dir()]
    bind = [] # first, last, local, total, title
    for thread in threads:
        info = "/".join([thread, meta[0]])
        replies = "/".join([thread, meta[1]])
        if not os.path.isfile(info):
            t = thread.split("/")[-1]
            orig = "/".join([friends[board], "raw",
                             "local", t, "head.txt"])
            u.wget(orig, info)
        with open(info, "r") as info:
            info = info.read()
        if len(info) == 0:
            continue 
        info = info.splitlines()[0]
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
    tdir = "/".join(["./threads", board])
    threads = [x.name for x in os.scandir(tdir) if x.is_dir()]
    for thread in threads:
        mkthread(board, thread)
    ldboard(board, 1)

def pullboard(board):
    f = s.friends
    if not board in f:
        return
    fn = arc + board + ".new"
    old = arc + board 
    url = "/".join([f[board], "raw", "local"])
    indurl = url + "/list.txt"
    newp = [x.split(" ") for x in
           u.wget(indurl, fn).splitlines()
           if x.strip()]
    if not os.path.exists(old):
        oldp = []
    else:     
        with open(old, "r") as oldp:
            oldp = [x.split(" ") for x in
               oldp.read().splitlines()
               if x.strip()]
    diff = [x[0] for x in newp if x not in oldp]
    if not diff:
        os.remove(fn)
        return
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
    tags.mkboard(board)

def mksite():
    fnames = list(friends.keys())
    threads = []
    for f in fnames:
        tfn = "/".join(["./threads", f, "list.txt"])
        with open(tfn, "r") as tind:
            tind = tind.read().splitlines()
        tind = [t.split(" ") for t in tind]
        tind = [[f, *t[0:4], " ".join(t[4:])] for t in tind]
        threads.append(tind)
    threads = sum(threads, [])
    threads = sorted(threads, key=lambda x: x[2], reverse=1)
    tf = "\n".join([" ".join(t) for t in threads])
    with open("./threads/list.txt", "w") as site:
        site.write(tf)
    tags.mksite(1)

def mkfriends():
    fs = [[f, friends[f]] for f in friends.keys()]
    f = "\n".join([" ".join(f) for f in fs])
    with open("./threads/friends.txt", "w") as flist:
        flist.write(f)

def linksites():
    mkfriends()
    furls = {friends[f]: f for f in friends}
    for f in friends:
        if f is "local":
            continue
        
        # furl - remote friendslist url
        # lurl - remote thread index url
        # ffn - friendslist filename (friends.board)
        # nffn - new friendslist filename (friends.board.new)
        # lfn - thread index filename (list.board)
        # nlfn - new thread index filename (list.board.new)
        # changes - threads with new replies from self
        # boards - boards that need their index rewritten
        
        furl = "/".join([friends[f], "raw", "friends.txt"])
        lurl = "/".join([friends[f], "raw", "list.txt"])
        ffn = arc + "friends." + f
        if not os.path.exists(ffn):
            with open(ffn, "w") as fi:
                fi.write("")
        nffn = ffn + ".new"
        lfn = arc + "list." + f
        if not os.path.exists(lfn):
            with open(lfn, "w") as fi:
                fi.write("")
        nlfn = lfn + ".new"
        u.wget(furl, nffn)
        u.wget(lurl, nlfn)

        # Ideally, a list of [name, op] localreplies
        # is compared against the older version, and
        # if a difference is found, {common}/{thread}/{friend}
        # is downloaded, {common}/{thread} & {common} are then
        # rebuilt. This is contingent on {common} being a common
        # board between client and server. 
        with open(nffn, "r") as nf:
            nf = nf.read().splitlines()
        nf = [x.split(" ") for x in nf]
        nfurls = {x[1]: x[0] for x in nf}
        common = {nfurls[x]: furls[x] for x in nfurls if x in furls}
        common2 = {common[f]: f for f in common}
        with open(lfn, "r") as oldl:
            oldl = [o.split(" ") for o in oldl.read().splitlines()]
        with open(nlfn, "r") as newl:
            newl = [n.split(" ") for n in newl.read().splitlines()]
        changes = []
        for n in newl:
            if n[0] not in common.keys():
                continue
            if not int(n[3]):
                continue
            if n in oldl:
                continue
            n = [common[n[0]], n[1], n[3]]
            changes.append(n)

        for c in changes:
            url = "/".join([friends[f], "raw", common2[c[0]],
                           c[1], "local.txt"])
            ldir = "/".join(["./threads", c[0], c[1]])
            local = "/".join([ldir, f + ".txt"])
            if not os.path.isdir(ldir):
                os.mkdir(ldir)
            u.wget(url, local)
            mkthread(c[0], c[1])
        boards = set([c[0] for c in changes])
        for b in boards:
            mkboard(b)
        os.rename(nffn, ffn)
        os.rename(nlfn, lfn)
    mksite()
    

def main():
    for f in friends:
        if f == "local":
            mkboard("local")
            continue
        if not os.path.isdir("./threads/" + f):
            os.mkdir("./threads/" + f)
        pullboard(f)
    mksite()
    linksites()
    mod.main()
    
if __name__ == "__main__":
    main()

# mkthread(board, thread)
#    modifies thread's list
# mkboard(board)
#    makes board/list.txt from mkboard in all subdirs
# mksite()
#    makes /list.txt from all board/list.txt
    
