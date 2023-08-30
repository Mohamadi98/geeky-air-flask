from database import connect
from services.loginService import getUserFromToken
from flask import jsonify

def charge_user(token, keyword):
    db_client, cur = connect()
    email = getUserFromToken(token)
    if isinstance(email, tuple) and len(email) == 2 and email[1] == 400:
        return email[0]

    query = 'SELECT balance FROM users WHERE email = %s'
    cur.execute(query, (email,))

    balance = cur.fetchone()[0]

    if keyword == 'modify':
        if balance < 1:
            return jsonify({
                'message': 'not enough balance'
            }), 400
        
        new_balance = balance - 1
        query2 = 'UPDATE users SET balance = %s WHERE email = %s;'
        cur.execute(query2, (new_balance, email))
        db_client.commit()

        cur.close()
        db_client.close()

        return True
    
    if keyword == 'shop':
        if balance < 0.5:
            return jsonify({
                'message': 'not enough balance'
            }), 400
        
        new_balance = balance - 0.5
        query2 = 'UPDATE users SET balance = %s WHERE email = %s;'
        cur.execute(query2, (new_balance, email))
        db_client.commit()

        cur.close()
        db_client.close()

        return True