from flask import Blueprint, request
import replicate
from dotenv import load_dotenv
import os
from services.loginService import verifyToken

load_dotenv()

imageRouter = Blueprint('imageHandler', __name__)
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_KEY')

@imageRouter.route('/image-generator')
def index():
    request_data = request.get_json()
    token = request_data.get('token')
    result = verifyToken(token)

    if result == True:

        prompt = request_data.get('prompt')
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={"prompt": prompt,
                "height": 640,
                "width": 640,
                "num_outputs": 1 
                }
        )
        return output
    
    else:
        return result