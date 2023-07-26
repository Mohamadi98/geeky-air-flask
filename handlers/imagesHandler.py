from flask import Blueprint, request, jsonify
import replicate
from dotenv import load_dotenv
import os
from services.loginService import verifyToken
from services.chargeUserService import charge_user

load_dotenv()

imageRouter = Blueprint('imageHandler', __name__)
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_KEY')

@imageRouter.route('/image-generator', methods = ['POST'])
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
        return jsonify({
            'URL': output
        })
    
    else:
        return result
    
# @imageRouter.route('/charge-user', methods = ['POST'])
# def charge():
#     request_data = request.get_json()
#     token = request_data.get('token')
#     return charge_user(token)

@imageRouter.route('/image-generate-surprise-me', methods = ['POST'])
def modify_generated_image_without_prompt():
    request_data = request.get_json()
    token = request_data.get('token')
    image_url = request_data.get('url')

    token_verification = verifyToken(token)

    if token_verification == True:
        output = replicate.run(
            "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
            input={
                "image": image_url,
                "prompt": "",
                "num_samples": "1",
                "image_resolution": "512",
                "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                }
        )
        return output[1]

    else:
        return token_verification
    
@imageRouter.route('/image-generate-modify')
def modify_generated_image_with_prompt():
    request_data = request.get_json()
    token = request_data.get('token')
    image_url = request_data.get('url')
    prompt = request_data.get('prompt')

    token_verification = verifyToken(token)

    if token_verification == True:
        output = replicate.run(
            "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
            input={
                "image": image_url,
                "prompt": prompt,
                "num_samples": "1",
                "image_resolution": "512",
                "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                }
        )
        return output[1]

    else:
        return token_verification