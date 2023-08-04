from database import connect

def check_email_exist(email):
    db_client, cur = connect()

    query = 'SELECT email FROM users WHERE email = %s'
    cur.execute(query, (email,))
    result = cur.fetchone()[0]
    cur.close()
    db_client.close()
    if not result:
        return False
    
    else:
        return True