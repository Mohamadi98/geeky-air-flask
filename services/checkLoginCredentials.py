from database import connect
from flask import jsonify
from services.passwordHash import verifyHash

def loginCredsCheck(username, password):
    db_client, cur = connect()
    query = f'SELECT * FROM users WHERE username = %s'
    cur.execute(query, (username,))
    result = cur.fetchone()
    if result == None:
        cur.close()
        db_client.close()
        return False
    
    # the result returned is a tuple without keys, the order of the password coloumn is second
    # hence index 1 is used to retrieve the password
    hashed_password = result[1]
    fetchedRole = result[5]

    if fetchedRole == 'admin':
        return fetchedRole
    
    if verifyHash(password, hashed_password):
        cur.close()
        db_client.close()
        return True
    
    else:
        cur.close()
        db_client.close()
        return False