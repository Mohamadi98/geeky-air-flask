from database import connect
from services.loginService import getUserFromToken
from flask import jsonify

def charge_user(token):
    db_client, cur = connect()
    username = getUserFromToken(token)
    if isinstance(username, tuple) and len(username) == 2 and username[1] == 400:
        return username[0]

    query = 'SELECT balance FROM users WHERE username = %s'
    cur.execute(query, (username,))

    balance = cur.fetchone()[0]

    if balance == 0:
        return jsonify({
            'message': 'not enough balance'
        }), 400
    
    new_balance = balance - 1
    query2 = 'UPDATE users SET balance = %s WHERE username = %s'
    cur.execute(query2, (new_balance, username))
    db_client.commit()

    cur.close()
    db_client.close()

    return jsonify({
        'message': 'user charged successfuly'
    })