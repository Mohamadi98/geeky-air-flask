from database import connect

def get_user_images(user_id):
    db_client, cur = connect()

    images_array = []
    query = 'SELECT image_url FROM image WHERE user_id = %s'
    cur.execute(query, (user_id,))
    results = cur.fetchall()

    cur.close()
    db_client.close()
    if not results:
        return ""
    
    else:
        for row in results:
            image = row[0]
            images_array.append(image)

        return images_array
