import os
import settings as s

tlist = s.tags
flist = s.friends

def mkboard(board):
    boardp = "/".join(["./threads", board])
    tagp = boardp + "/tags.txt"
    threads = [x.path for x in os.scandir(boardp) if x.is_dir()]
    tagd = {}
    for thread in threads:
        num = thread.split("/")[3]
        head = thread + "/head.txt"
        with open(head, "r") as head:
            tags = head.read().splitlines()
        try:
            tags = tags[1].split(" ")
        except:
            tags = ["random"]
        for t in tags:
            if t not in tlist:
                continue
            if t not in tagd:
                tagd[t] = []
            tagd[t].append(num)
    print(tagd)
    tagf = [" ".join([t, *tagd[t]]) for t in tagd]
    with open(tagp, "w") as tags:
        tags.write("\n".join(tagf))
    return

def mksite():
    tdb = {x: [] for x in tlist}
    for f in flist:
        print(f)
        mkboard(f)
        
        tpath = "/".join(["./threads", f, "tags.txt"])
        with open(tpath, "r") as tag:
            tag = tag.read().splitlines()
        tag = [x.split(" ") for x in tag]
        tag = {x[0]: x[1:] for x in tag}
        for t in tag:
            tag[t] = [[f, x] for x in tag[t]]
            tdb[t].append(tag[t])
    for t in tdb:
        tdb[t] = [y for x in tdb[t] for y in x]
        print(t, len(tdb[t]))
#    print(tdb)
    return

mksite()
