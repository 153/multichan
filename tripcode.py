import settings as s
import crypt
import sys

def mk(pw):
    sect = ""
    pw = pw[:8]
    salt = (pw + "H.")[1:3]
    trip = crypt.crypt(pw, salt)
    return trip[-10:]

def sec(pw):
    print(pw)
    pw = pw[:10]
    salt = s.salt
    trip = crypt.crypt(pw, salt)
    return trip[-12:]

if __name__ == "__main__":
    print(" !" + mk(sys.argv[1]))
    print(" !!" + sec(sys.argv[1]))

