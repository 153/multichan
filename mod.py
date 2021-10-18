import os
import shutil
import tags
import refresh
import settings as s

def del_comment(host, thread, site, reply):
    path = "/".join(["./threads", host, thread, site]) + ".txt"
    with open(path, "r") as comments:
        comments = comments.read().splitlines()
    reply = int(reply) - 1
    comments[reply] = comments[reply].split("<>")
    comments[reply][1] = "Deleted"
    comments[reply][2] = "<i>this comment was deleted</i>"
    comments[reply] = "<>".join(comments[reply])
    comments = "\n".join(comments) + "\n"
    with open(path, "w") as path:
        path.write(comments)

def del_thread(host, thread):
    path = "/".join(["./threads", host, thread])
    hlistp = "/".join(["./threads", host, "list"]) + ".txt"
    with open(hlistp, "r") as hlist:
        hlist = hlist.read().splitlines()
    hlist = [b for b in hlist if b.split(" ")[0] != thread]
    hlist = "\n".join(hlist)
    with open(hlistp, "w") as hlistp:
        hlistp.write(hlist)
    shutil.rmtree(path)
    refresh.ldhost(board, host)
    refresh.mksite()

def main():
    with open(s.delete, "r") as delete:
        delete = delete.read().splitlines()
    delete = [d.split(";")[0] if ";" in d else d for d in delete]
    delete = [d.strip().split(" ") for d in delete]
    for d in delete:
        try:
            if len(d) == 2:
                del_thread(*d)
            elif len(d) == 4:
                del_comment(*d[:3], int(d[3]))
            if d > 1:
                print(d)
        except:
            pass
    tags.mksite(1)

if __name__ == "__main__":
    main()
