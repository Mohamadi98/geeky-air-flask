from database import connect
from flask import jsonify
from services.updatePassword import updatePass
from services.passwordHash import hashFunc

def forgetPass(email, password):
    db_client, cur = connect()
    query = 'SELECT * FROM users WHERE email = %s'
    cur.execute(query, (email,))
    result = cur.fetchone()
    if result == None:
        return jsonify({'message': 'No account associated with this email'})
    
    hashedPassword = hashFunc(password)
    
    return updatePass(email, hashedPassword)
