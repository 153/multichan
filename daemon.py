import time
import threading
import refresh
import settings

def linker():
    cnt = 0
    while True:
        refresh.linksites()        
        cnt += 1
        print(cnt)    
        time.sleep(settings.refreshtime)

def run():
    d = threading.Thread(target=linker)
    d.start()
