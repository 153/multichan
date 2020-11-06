import os

def ldsing(board, thread, sub):
    tdir = "/".join(["./threads", board, thread])
    tf = tdir + "/" + sub + ".txt"
    with open(tf, "r") as tf:
        tf = tf.read().splitlines()
    tf = [x.split("<>")[0] for x in tf]
    return tf

def mkthread(board, thread):
    d = ["head.txt", "list.txt"]
    tdir = "./threads/" + board + "/" + thread
    reps = os.listdir(tdir)
    reps = [r for r in reps if r not in d]
    reps = [r.split(".")[0] for r in reps]
    reps = [r for r in reps if len(r)]
    threads = {}
    posts = []        
    for r in reps:
        threads[r] = ldsing(board, thread, r)
    for r in threads:
        for p in threads[r]:
            posts.append([r, p])
    posts = sorted(posts, key=lambda x: x[1])
    posts = [" ".join(p) for p in posts]
    posts = "\n".join(posts)
    lf = tdir + "/list.txt"
    with open(lf, "w") as lf:
        lf.write(posts)

def ldboard(board):
    # Generate new board index based on existing thread indexes.
    meta = ["head.txt", "list.txt"]
    tdir = "./threads/" + board
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
    return bind
    
ldboard("local")  
ldboard("00chan")

# threads/local/1602486291
# mkthread("local", "1602486291")
# print( "=" * 20)
# threads/00chan/1602225514
# mkthread("00chan", "1602225514")
