import time
import threading
import refresh

def linker():
    cnt = 0
    while True:
        refresh.linksites()        
        cnt += 1
        print(cnt)    
        time.sleep(60*15)

def run():
    d = threading.Thread(target=linker)
    d.start()
