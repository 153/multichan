import settings as s
import os
import shutil

files = ["./settings.py", "./threads/", "./html/", "./static/",
         s.archive, s.wlist, s.log, s.bans, s.delete]
loc = s.backup

if not os.path.isdir(loc):
    os.mkdir(loc)
    
def copy(src, dst):
    try:
        shutil.copytree(src, dst + src)
    except:
        shutil.copy(src, dst)

for f in files:
    copy(f, loc)
