name = "multich"
url = "http://localhost"
_port = 5150

archive = "./archive/"

wlist = "./ips.txt"
log = "./log.txt"
delete = "./delete.txt"
bans = "./bans.txt"
logcomment = True

tags = ["random",  "nsfw"]
_short = 120
_long = 10000

images = True
ihost = "https://i.imgur.com/"
torport = 9050

refreshtime = 60*15 # Check friend boards every 15 minutes
friends = {
    "0chan": "http://0chan.vip",
    "52chan": "http://bbs.4x13.net",
    "ripirc": "http://ripirc.org",
    "kuzlol": "http://multich.kuz.lol",
    "local": url
    }

# secure tripcode hash
salt = "heoiehtiheohteohte"

# password sha256 hash : "changeme"
# not used yet! x
phash = "057ba03d6c44104863dc7361fe4578965d1887360f90a0895882e58a6248fc86"
