import time
import urllib.request

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
        

#print(otnow, unix2hum(tnow))
