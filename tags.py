import os
from flask import Blueprint, request
import settings as s
import pagemaker as p

tags = Blueprint("tags", __name__)
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
        if len(threads) and threads != [""]:
            tagdb[tag] = threads
        else:
            tagdb[tag] = []
    return tagdb

def tags_view(tags=[]):
    db = tags_load()
    threads = []    
    tmp = []
    for t in tags:
        if t in db:
            tmp += db[t]
        else:
            tmp += []
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
                tagd[t] = []
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
            if t not in tdb:
                tdb[t] = []
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

@tags.route('/tags/')
def tag_index():
    tdb = tags_load()
    sentry = "<li><b><a href='/tags/{0}/'>{0}</a></b> ({1})"
    oentry = "<li><a href='/tags/{0}/'>{0}</a> ({1})"
    result =  ["<h1>Conversation tags</h1>",
               "Bolded tags are the default tags selected by the site admin."]
    links = ["<ul>"]
    site_tags = {t : len(tdb[t]) for t in tlist}
    site_tags = {k: v for k, v in sorted(site_tags.items(),
                                         key= lambda x: int(x[1]))[::-1]}
    all_tags = {t : len(tdb[t]) for t in list(tdb.keys()) if t not in tlist}
    all_tags = {k: v for k, v in sorted(all_tags.items(),
                                         key= lambda x: int(x[1]))[::-1]}
    

    for t in site_tags:
        links.append(sentry.format(t, site_tags[t]))
    links.append("</ul><ul>")
    for t in all_tags:
        links.append(oentry.format(t, all_tags[t]))
    links.append("</ul>")
    result.append("\n".join(links))
    result = p.mk("\n".join(result))
    return result
    
    
# tags_load() -> db
# tags_view([]) -> threads


#print("\n0chan:")
#tags_load("0chan")
