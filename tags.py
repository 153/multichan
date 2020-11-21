import os
import settings as s

tlist = s.tags

def mkboard(board):
    boardp = "/".join(["./threads", board])
    tagp = boardp + "/tags.txt"
    threads = [x.path for x in os.scandir(boardp) if x.is_dir()]
    tagd = {}
    for thread in threads:
        num = thread.split("/")[3]
        head = thread + "/head.txt"
        with open(head, "r") as head:
            tags = head.read().splitlines()[1].split(" ")
        for t in tags:
            print(t)
            if t not in tlist:
                continue
            if t not in tagd:
                tagd[t] = []
            tagd[t].append(num)
        print(board, num, tags)
    print(tagd)
    tagf = [" ".join([t, *tagd[t]]) for t in tagd]
    print("\n".join(tagf))
    with open(tagp, "w") as tags:
        tags.write("\n".join(tagf))
    return

mkboard("local")

def mksite():
    return
