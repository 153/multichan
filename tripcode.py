import crypt

def mk(pw):
    pw = pw[:8]
    salt = (pw + "H.")[1:3]
    trip = crypt.crypt(pw, salt)
    return trip[-10:]
