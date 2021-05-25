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

def del_thread(board, thread):
    path = "/".join(["./threads", board, thread])
    blistp = "/".join(["./threads", board, "list"]) + ".txt"
    with open(blistp, "r") as blist:
        blist = blist.read().splitlines()
    blist = [b for b in blist if b.split(" ")[0] != thread]
    blist = "\n".join(blist)
    with open(blistp, "w") as blistp:
        blistp.write(blist)
    shutil.rmtree(path)
    refresh.ldboard(board, 1)
    refresh.mksite()

def main():
    with open(s.delete, "r") as delete:
        delete = delete.read().splitlines()
    delete = [d.split(";")[0] if ";" in d else d for d in delete]
    delete = [d.split(" ") for d in delete]
    for d in delete:
        print(d)
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
