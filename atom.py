import time
import settings as s

tstring = "%Y-%m-%dT%H:%M:%S+00:00"

fn = "./static/threads.atom"
url = s.url
title = s.name
index = "threads/local/list.txt"

feed = {}
feed["title"] = " ".join([title, "@", url])
feed["id"] = url
feed["entries"] = []

feed_temp = """<?xml version="1.0" encoding="utf-8"?>
  <feed xmlns="http://www.w3.org/2005/Atom">
<title>{title}</title>
<author><name>Anonymous</name></author>
<id>{id}</id>
<link rel="self" href="{link}" />
<updated>{published}</updated>
"""

entry_temp = """  <entry>
<title>{title}</title>
<link rel="alternate" href="{url}" />
<id>{url}</id>
<published>{published}</published>
<updated>{published}</updated>
<content type="text">
{content}
</content>
  </entry>"""

def mkthreads():
    feed["link"] = url + "/threads.atom"
    with open(index, "r") as tind:
        tind = tind.read().splitlines()

    # Make an index of local threads by sorting them by
    # newest created thread sorted to oldest. This is more
    # useful for ATOM feeds than sorting by bumps, and
    # makes more sense than a global thread feed
    # (which may come later).
    
    tind = [t.split(" ") for t in tind]
    tind = sorted(tind)[::-1]
    tind = [[*t[:4], " ".join(t[4:])] for t in tind]

    for t in tind:
        entry = {}
        entry["title"] = t[-1]
        entry["url"] = link = url + "/threads/local/" + t[0]
        entry["published"] = time.strftime(tstring, time.localtime(int(t[0])))
        entry["fn"] = "./threads/local/" + t[0] + "/local.txt"
        with open(entry["fn"], "r") as content:
            content = content.read().splitlines()[0].split("<>")[2:]
        entry["content"] = "<>".join(content)
        entry["content"] = entry["content"]\
            .replace("<br>", "\n").replace("<", "&lt;").replace(">", "&gt;")
        feed["entries"].append(entry)

    feed["published"] = feed["entries"][0]["published"]    

    atompage = []
    atompage.append(feed_temp.format(**feed))
    for entry in feed["entries"]:
        atompage.append(entry_temp.format(**entry))
    atompage.append("  </feed>")
    atompage = "\n".join(atompage)
    
    with open(fn, "w") as atom:
        atom.write(atompage)
        
if __name__ == "__main__":
    mkthreads()
