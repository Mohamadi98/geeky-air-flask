from database import connect

def addBalance(amount, username):
    try:
        db_client, cur = connect()
        retreiving_query = 'SELECT balance FROM users WHERE username = %s'
        cur.execute(retreiving_query, (username,))
        fetched_balance = cur.fetchone()[0]
        new_balance = fetched_balance + float(amount)
        adding_query = 'UPDATE users SET balance = %s WHERE username = %s'
        cur.execute(adding_query, (new_balance, username))
        db_client.commit()
        cur.close()
        db_client.close()

        return True
    
    except Exception as e:
        return f'an error occurred: {e}'