from database import connect

def addBalance(amount, username):
    try:
        db_client, cur = connect()
        query = 'UPDATE users SET balance = %s WHERE username = %s'
        cur.execute(query, (amount, username))
        db_client.commit()
        cur.close()
        db_client.close()
    
    except Exception as e:
        return f'an error occurred: {e}'