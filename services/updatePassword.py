from database import connect
from flask import jsonify

def updatePass(email, password):
    print(password)
    db_client, cur = connect()
    cur.execute('UPDATE users SET password = %s WHERE email = %s', (password, email))
    db_client.commit()
    cur.close()
    db_client.close()

    return jsonify({'message': 'password updated successfuly'})