import time
import threading
import refresh
import settings
import mod
import atom

def linker():
    cnt = 0
    while True:
        refresh.linksites()
        try:
            mod.main()
        except:
            pass
        atom.mkthreads()
        cnt += 1
        print(cnt)
        
        time.sleep(settings.refreshtime)

def run():
    d = threading.Thread(target=linker)
    d.start()
