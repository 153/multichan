name = "multich"
url = "http://localhost"
_port = 5150

# These are the suggested #tags for new posts
tags = ["random",  "nsfw"]

# Salt -- used for secure tripcode
# Admin password -- SHA256("changeme") - Not used yet
salt = "changeme"
phash = "057ba03d6c44104863dc7361fe4578965d1887360f90a0895882e58a6248fc86"

archive = "./archive/" # Used for federation
backup = "./bak/"      # Used with ./backup.py
wlist = "./ips.txt"
log = "./log.txt"
delete = "./delete.txt"
bans = "./bans.txt"
logcomment = True      # Whether to store full comment in log.txt

_short = 120   # Name, title, tag field 
_long = 10000  # Post message field

images = False
ihost = "https://i.imgur.com/"
boards = False

# Tor needs to be installed and pip3 install requests_tor package.
# Only used for .onion friends
torport = 9050

refreshtime = 60*15 # Check friend boards every 15 minutes
friends = {
    "0chan": "http://0chan.vip",
    "52chan": "http://bbs.4x13.net",
    "ripirc": "http://ripirc.org",
    "kuzlol": "http://multich.kuz.lol",
    "local": url
    }
