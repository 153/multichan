import time

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


#print(otnow, unix2hum(tnow))
