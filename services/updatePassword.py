from database import connect
from flask import jsonify

def updatePass(email, password):
    db_client, cur = connect()
    query = 'UPDATE users SET password = %s WHERE email = %s'
    cur.execute(query, (password, email))
    db_client.commit()
    cur.close()
    db_client.close()

    return jsonify({'message': 'password updated successfuly'})