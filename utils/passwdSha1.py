import hashlib

Code = "utf-8"

def Sha1Translate(password):
    passworded = hashlib.sha1(password.encode(Code)).hexdigest()
    return passworded

if __name__ == '__main__':
    s = Sha1Translate("z258330500")
    print(s)