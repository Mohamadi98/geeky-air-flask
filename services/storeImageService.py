from database import connect
from flask import jsonify
from services.loginService import getUserFromToken

def store_image(token, image_url):
    db_client, cur = connect()

    username = getUserFromToken(token)
    if isinstance(username, tuple) and len(username) == 2 and username[1] == 400:
        return username[0]
    
    query = 'SELECT id FROM users WHERE username = %s'
    cur.execute(query, (username,))
    result = cur.fetchone()[0]

    query2 = 'INSERT INTO image (user_id, image_url) VALUES (%s, %s)'
    cur.execute(query2, (result, image_url))
    db_client.commit()

    cur.close()
    db_client.close()

    return True
