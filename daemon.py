import time
import refresh

cnt = 0
while True:
    cnt += 1
    print(cnt)
    
    time.sleep(60 * 30)
    refresh.linksites()
