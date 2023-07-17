from database import connect

def addBalance(amount, username):
    try:
        db_client, cur = connect()
        query = f'UPDATE users SET balance = {amount} WHERE username = %S'
        cur.execute(query, (username,))
        db_client.commit()
        cur.close()
        db_client.close()
    
    except Exception as e:
        return f'an error occurred: {e}'