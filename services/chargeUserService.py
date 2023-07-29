from database import connect
from services.loginService import getUserFromToken
from flask import jsonify

def charge_user(token):
    db_client, cur = connect()
    email = getUserFromToken(token)
    print(email)
    if isinstance(email, tuple) and len(email) == 2 and email[1] == 400:
        return email[0]

    query = 'SELECT balance FROM users WHERE email = %s'
    cur.execute(query, (email,))

    balance = cur.fetchone()[0]
    print(type(balance))
    print('the initial balance: ', balance)

    if balance == 0.0:
        return jsonify({
            'message': 'not enough balance'
        }), 400
    
    new_balance = balance - 1.0
    print('the new balance after deduction: ', new_balance)
    query2 = 'UPDATE users SET balance = %s WHERE username = %s'
    cur.execute(query2, (new_balance, email))
    db_client.commit()

    cur.close()
    db_client.close()

    return True