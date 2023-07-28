from database import connect

def addBalance(amount, email):
    try:
        db_client, cur = connect()
        retreiving_query = 'SELECT balance FROM users WHERE email = %s'
        cur.execute(retreiving_query, (email,))
        fetched_balance = cur.fetchone()[0]
        new_balance = fetched_balance + float(amount)
        adding_query = 'UPDATE users SET balance = %s WHERE email = %s'
        cur.execute(adding_query, (new_balance, email))
        db_client.commit()
        cur.close()
        db_client.close()

        return True
    
    except Exception as e:
        return f'an error occurred: {e}'