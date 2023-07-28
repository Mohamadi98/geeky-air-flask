from database import connect
from flask import jsonify
from services.loginService import getUserFromToken

def store_image(token, image_url):
    db_client, cur = connect()

    email = getUserFromToken(token)
    if isinstance(email, tuple) and len(email) == 2 and email[1] == 400:
        return email[0]
    
    query = 'SELECT id FROM users WHERE email = %s'
    cur.execute(query, (email,))
    result = cur.fetchone()[0]

    query2 = 'INSERT INTO image (user_id, image_url) VALUES (%s, %s)'
    cur.execute(query2, (result, image_url))
    db_client.commit()

    cur.close()
    db_client.close()

    return True
