import requests
import json
from dotenv import load_dotenv
import os
from flask import jsonify

load_dotenv()

api_key = os.getenv('GOOGLE_LENS_KEY')
api_url = 'https://serpapi.com/search?engine=google_lens'



def google_lens_request(image):
    try:
        params = {
        "engine": "google_lens",
        "url": image,
        "api_key": api_key
        }
        response = requests.get(url=api_url, params=params)
        data = json.loads(response.content)
        array = data["visual_matches"]
        results_array = []
        for match in array:
            if 'price' in match:
                link = match['link']
                thumbnail_url = match['thumbnail']
                price = match['price']['extracted_value']
                description = match['title']
                obj1 = {
                    'link': link,
                    'thumbnail': thumbnail_url,
                    'price': price,
                    'description': description
                }
                results_array.append(obj1)
            else:
                continue
        
        if (len(results_array) == 0):
            print('empty array')
        return jsonify({
            'data': results_array[0]
        })
    
    except Exception as e:
        return f'this is the ERROR: {e}'