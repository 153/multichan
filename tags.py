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
            if tag in tagdb:
                tagdb[tag] += [t for t in threads if t not in tagdb[tag]]
                print(tagdb[tag])
            else:
                tagdb[tag] = threads
        else:
            tagdb[tag] = []
    return tagdb

def tags_threads(tags=[]):
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
    sentry = "<li><b><a href='/tags/{0}/'>{0}</a></b> ({1} discussions)"
    oentry = "<li><a href='/tags/{0}/'>{0}</a> ({1} discussions)"
    result =  ["<h1>Conversation tags</h1>",
               "Bolded tags are the default tags selected by the site admin."]
    result.append("<br>Tags can be combined with the '+' plus sign in URL.")
    links = ["<ul>"]
    site_tags = {t : len(tdb[t]) for t in tlist}
    site_tags = {k: v for k, v in sorted(site_tags.items(),
                                         key= lambda x: int(x[1]))[::-1]}
    all_tags = {t : len(tdb[t]) for t in list(tdb.keys()) if t not in tlist}
    all_tags = {k: v for k, v in sorted(all_tags.items(),
                                         key= lambda x: int(x[1]))[::-1]}
    
    for t in site_tags:
        links.append(sentry.format(t, site_tags[t]))
        if site_tags[t] == 1:
            links[-1] == links[-1].replace("s)", ")")
    links.append("</ul><ul>")
    cnt = 0
    last = 0
    for t in all_tags:
        cnt = int(all_tags[t])
        if (cnt < last) and (cnt == 1):
            links.append("</ul><ul>")
        links.append(oentry.format(t, all_tags[t]))
        if all_tags[t] == 1:
            links[-1] = links[-1].replace("s)", ")")
        last = cnt
    links.append("</ul>")
    result.append("\n".join(links))
    result = p.mk("\n".join(result))
    return result

@tags.route('/tags/<topic>/')
def tag_page(topic):
    line = "<tr><td>{0} " \
    + "<td><a href='/threads/{0}/{1}'>{5}</a>" \
    + "<td>{4}"
    result = []
    ot = "".join(topic)
    if "+" in topic:
        topic = topic.split("+")
    else:
        topic = [topic]
    result.append("<h1> #" + " #".join(topic) + "</h1>")
    result.append(" <a href='/create/" + ot + "'>+ create new</a><br>")
    result.append("<i>Note: tags can be combined using the "
                  "+ (plus sign) in the URL</i>")
    result.append("<p><table>")
    result.append("<tr><th>origin<th>title<th>replies")
    threads = tags_threads(topic)
    with open("./threads/list.txt") as site:
        site = site.read().splitlines()
    site = [s.split(" ") for s in site]
    site = [[*s[:5], " ".join(s[5:])] for s in site
            if [s[0], s[1]] in threads]
    result[0] += " (" + str(len(site)) + " threads)</h1>"
    test = "\n".join([line.format(*t) for t in site])
    result.append(test)
    result.append("</table>")
    result = p.mk("\n".join(result))
    return result

if __name__ == "__main__":
    mksite(1)

# tags_load() -> db
# tags_threads([]) -> threads
# mkboard()
# mksite()
# tag_index()

#print("\n0chan:")
#tags_load("0chan")
