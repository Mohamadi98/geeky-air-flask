from database import connect
from flask import jsonify

class user:
    def __init__(self, username = None, password = None, balance = 0.0, email = None, role = 'user'):
        self.username = username
        self.password = password
        self.balance = balance
        self.email = email
        self.role = role

    def create(userObj):
        db_client, cur = connect()
        cur.execute('INSERT INTO users (username, email, password, balance, role) VALUES (%s, %s, %s, %s, %s)', 
                    (userObj.username, userObj.email, userObj.password, userObj.balance, userObj.role))
        db_client.commit()
        cur.close()
        db_client.close()
        
        return jsonify({'message': 'User created successfully'}), 200
        