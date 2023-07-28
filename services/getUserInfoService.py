from database import connect
from services.loginService import getUserFromToken
from flask import jsonify

def get_user_info(token):
    db_client, cur = connect()

    email = getUserFromToken(token)
    if isinstance(email, tuple) and len(email) == 2 and email[1] == 400:
        return email[0]
    
    query = 'SELECT username, email, balance FROM users WHERE email = %s;'
    cur.execute(query, (email,))
    result = cur.fetchone()
    if result is None:
        return jsonify({
            'message': 'user does not exist'
        })
    
    cur.close()
    db_client.close()
    
    name = result[0]
    email = result[1]
    balance = result[2]

    return jsonify({
        'username': name,
        'email': email,
        'balance': balance
    })