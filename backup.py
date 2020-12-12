import os
import shutil

files = ["./settings.py", "./ips.txt", "./log.txt", "./threads/"]
loc = "./bak/"
if not os.path.isdir(loc):
    os.mkdir(loc)
    
def copy(src, dst):
    try:
        shutil.copytree(src, dst + "threads/")
    except:
        shutil.copy(src, dst)

for f in files:
    copy(f, loc)
