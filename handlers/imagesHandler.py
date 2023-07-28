from flask import Blueprint, request, jsonify
import replicate
from dotenv import load_dotenv
import os
from services.loginService import verifyToken
from services.chargeUserService import charge_user
from services.storeImageService import store_image
from services.saveImageToUploads import save_base64_image, delete_image_from_uploads

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

@imageRouter.route('/modify-image-upload', methods = ['POST'])
def modify_image_upload():
    request_data = request.get_json()
    if 'prompt' in request_data:
        prompt = request_data.get('prompt')

    else:
        prompt = ""

    token = request_data.get('token')
    image = request_data.get('image')

    token_verification = verifyToken(token)

    if token_verification == True:
        if len(image) < 200:
            # the image is a url
            output = replicate.run(
                "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                input={
                    "image": image,
                    "prompt": prompt,
                    "num_samples": "1",
                    "image_resolution": "512",
                    "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                    }
            )
            new_image_url =  output[1]

            charge_confirm = charge_user(token)

            if charge_confirm == True:
                return jsonify({
                    'URL': new_image_url
                })
            else:
                return charge_confirm
                
    
        else:
            # the image is a base64 image
            save_base64_image(image, f'{token}.jpg')
            output = replicate.run(
                "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                input={
                    "image": open(os.path.join('uploads', f'{token}.jpg'), 'rb'),
                    "prompt": prompt,
                    "num_samples": "1",
                    "image_resolution": "512",
                    "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                    }
            )
            new_image_url =  output[1]


            deletion_confirm = delete_image_from_uploads(f'{token}.jpg')
            charge_confirm = charge_user(token)

            if deletion_confirm:
                if charge_confirm:
                    return jsonify({
                        'URL': new_image_url
                    })
                else:
                    charge_confirm
                
            else:
                return deletion_confirm


    else:
        return token_verification