import bcrypt

def hashFunc(password):
    salt = bcrypt.gensalt()
    if password is None:
        print('password is none')
    if not isinstance(password, str):
        print('password is not a string')
    encodedPassword = password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(encodedPassword, salt)
    return hashedPassword.decode('utf-8')

def verifyHash(password, hashedPassword):
    encodedPassword = password.encode('utf-8')
    encodedHashedPassword = hashedPassword.encode('utf-8')
    return bcrypt.checkpw(encodedPassword, encodedHashedPassword)