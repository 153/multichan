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
    threads = {}
    posts = []    
    tdir = "./threads/" + board + "/" + thread
    reps = os.listdir(tdir)
    reps = [r for r in reps if r not in d]
    reps = [r.split(".")[0] for r in reps]
    reps = [r for r in reps if len(r)]
    
    for r in reps:
        threads[r] = ldsing(board, thread, r)
        print(r, ":", len(threads[r]))
    for r in threads:
        for p in threads[r]:
            posts.append([r, p])
    posts = sorted(posts, key=lambda x: x[1])
    for p in posts:
        print(" ".join(p))
    

# threads/local/1602486291
mkthread("local", "1602486291")

print( "=" * 20)
# threads/00chan/1602225514
mkthread("00chan", "1602225514")
