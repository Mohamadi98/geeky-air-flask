from services.updatePassword import updatePass
from services.passwordHash import hashFunc
from services.loginService import getUserFromToken, verifyToken

def forgetPass(token, password):
    check_token = verifyToken(token)
    if check_token != True:
        return check_token
    
    email = getUserFromToken(token)
    print(password)
    hashedPassword = hashFunc(password)
    print(hashedPassword)
    
    return updatePass(email, hashedPassword)
