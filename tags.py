import os
import settings as s

tlist = s.tags
flist = s.friends

# tags_board("board")
# tags_load()

# tags_view(["tags"])
# tags_addthread("num", ["tags"])

def tags_load(board=""):
    tagp = "/".join(["./threads", board, "tags.txt"])
    with open(tagp, "r") as tags:
        tags = tags.read().splitlines()
    tags = [x.split(" ") for x in tags]
    tagdb = {}
    for t in tags:
        tag = t[0]
        threads = t[1:]
        if "-" in threads[0]:
            threads = [x.split("-") for x in threads]
        tagdb[tag] = threads
    return tagdb

def tags_view(tags=[]):
    db = tags_load()
    threads = []    
    tmp = []
    for t in tags:
        tmp += db[t]
    for t in tmp:
        if t not in threads and len(t):
            threads.append(t)
    return threads
    
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
    tagf = [" ".join([t, *tagd[t]]) for t in tagd]
    with open(tagp, "w") as tags:
        tags.write("\n".join(tagf))
    return

def mksite(remake=0):
    tdb = {x: [] for x in tlist}
    for f in flist:
        if remake:
            mkboard(f)        
        tpath = "/".join(["./threads", f, "tags.txt"])
        with open(tpath, "r") as tag:
            tag = tag.read().splitlines()
        tag = [x.split(" ") for x in tag]
        tag = {x[0]: x[1:] for x in tag}
        for t in tag:
            tag[t] = [[f, x] for x in tag[t]]
            tdb[t].append(tag[t])
    tagl = []
    for t in tdb:
        tdb[t] = [y for x in tdb[t] for y in x]
        entry = " ".join(["-".join(x) for x in tdb[t]])
        tagl.append(" ".join([t, entry]))
    tagl = "\n".join(tagl)
    with open("./threads/tags.txt", "w") as tagf:
        tagf.write(tagl)    
    return

#mksite()
#print(tags_load())
tags_view(["meta", "nsfw", "life"])
#print("\n0chan:")
#tags_load("0chan")
