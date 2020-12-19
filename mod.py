import os
import shutil
import init

def del_comment(host, thread, site, reply):
    path = "/".join(["./threads", host, thread, site]) + ".txt"
    with open(path, "r") as comments:
        comments = comments.read().splitlines()
    reply = int(reply) - 1
    comments[reply] = comments[reply].split("<>")
    comments[reply][1] = "Deleted"
    comments[reply][2] = "<i>this comment was deleted</i>"
    comments[reply] = "<>".join(comments[reply])
    comments = "\n".join(comments)
    with open(path, "w") as path:
        path.write(comments)
    print(comments)

def del_thread(thread):
    path = "/".join(["./threads", "local", thread])
    blistp = "/".join(["./threads", "local", "list"]) + ".txt"
    with open(blistp, "r") as blist:
        blist = blist.read().splitlines()
    blist = [b for b in blist if b.split(" ")[0] != thread]
    blist = "\n".join(blist)
    with open(blistp, "w") as blistp:
        blistp.write(blist)
    shutil.rmtree(path)
    print(blist)

#del_thread("1608368801")
del_comment("52chan", "1608311210", "local", 1)
