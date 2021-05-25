import settings as s
import crypt

def mk(pw):
    pw = pw[:8]
    salt = (pw + "H.")[1:3]
    trip = crypt.crypt(pw, salt)
    return trip[-10:]

def sec(pw):
    pw = pw[:10]
    salt = s.salt
    trip = crypt.crypt(pw, salt)
    return trip[-12:]

if __name__ == "__main__":
    print(sec("faggot"))
