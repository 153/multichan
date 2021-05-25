import time
import urllib.request
import settings as s

tstring = "%Y-%m-%d %H:%M"

def unix2hum(unix):
    unix = int(unix)
    return time.strftime(tstring, time.localtime(unix))

def lines(filen):
    with open(filen, "r") as filen:
        filen = filen.read().splitlines()
    filen = [x for x in filen if len(x.strip())]
    return len(filen)

def pclean(post):
    post = post.split("<br>")

def wget(url, fn, w=1):
    try:
        page = urllib.request.urlopen(url)
        page = page.read().decode('utf-8')
    except:
        page = ""
    if not w:
        return page
    with open(fn, "w") as fn:
        fn.write(page)
    return page

def imgur(inp):
    host = "https://i.imgur.com/"
    img = inp.split(host)[1]
    if not s.images:
        return inp
    
    if " " or "<" in img:
        term = len(img)
        if 0 < img.find(" "):
            term = img.find(" ")
        if 0 < img.find("<") < term:
            term = img.find("<")
        img = img[:term]
    if (len(img) < 15) and ("." in img):
        img = host + img
        img2 = f"<a href='{img}'><img src='{img}'></a>"
        inp = inp.replace(img, " ", 1)
        inp = "<br><br>".join([img2, inp])
    
    return inp

#print(otnow, unix2hum(tnow))
