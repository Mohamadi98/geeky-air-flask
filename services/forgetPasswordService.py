from database import connect
from flask import jsonify
from services.updatePassword import updatePass
from services.passwordHash import hashFunc, verifyHash

def forgetPass(email, password):
    db_client, cur = connect()
    query = 'SELECT password FROM users WHERE email = %s'
    cur.execute(query, (email,))
    result = cur.fetchone()
    if result == None:
        return jsonify({'message': 'No account associated with this email'})
    
    fetchedPassword = result[0]
    if verifyHash(password, fetchedPassword):
        return jsonify({'message': 'you already signed up with this password'})
    
    hashedPassword = hashFunc(password)
    
    return updatePass(email, hashedPassword)
