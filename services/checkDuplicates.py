from database import connect

def check(data, flag):
    returnValue = False
    db_client, cur = connect()

    cur.execute('SELECT * FROM users WHERE %s = %s', (flag, data))
    result = cur.fetchone() 
    if result is not None:
        returnValue = True
    cur.close()
    db_client.close()

    return returnValue
        