from services.updatePassword import updatePass
from services.passwordHash import hashFunc
from services.loginService import getUserFromToken, verifyToken

def forgetPass(token, password):
    check_token = verifyToken(token)
    if check_token != True:
        return check_token
    
    email = getUserFromToken(token)
    hashedPassword = hashFunc(password)
    
    return updatePass(email, hashedPassword)
