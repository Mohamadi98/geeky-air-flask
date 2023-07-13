from database import connect

def check(data, flag):
    returnValue = False
    db_client, cur = connect()

    query = f'SELECT * FROM users WHERE {flag} = %s'
    cur.execute(query, (data,))    
    result = cur.fetchone()
    if result is not None:
        returnValue = True
    cur.close()
    db_client.close()

    return returnValue
        