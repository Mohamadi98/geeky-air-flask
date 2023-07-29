from flask import Blueprint, request, jsonify
import replicate
from dotenv import load_dotenv
import os
from services.loginService import verifyToken, getUserFromToken
from services.chargeUserService import charge_user
from services.saveImageToUploads import save_base64_image, delete_image_from_uploads, check_image_exist

load_dotenv()

imageRouter = Blueprint('imageHandler', __name__)
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_KEY')

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
    user_email = getUserFromToken(token)

    if token_verification == True:
        charge_confirm = charge_user(token)
        if charge_confirm == True:
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

                return jsonify({
                    'URL': new_image_url
                })
                    
        
            else:
                # the image is a base64 image
                save_base64_image(image, f'{user_email}.jpg')
                check_image_exist(f'{user_email}.jpg')
                image_path = os.path.join('uploads', f'{user_email}.jpg')
                print(image_path)
                # output = replicate.run(
                #     "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                #     input={
                #         "image": open(os.path.join('uploads', f'{user_email}.jpg'), 'rb'),
                #         "prompt": prompt,
                #         "num_samples": "1",
                #         "image_resolution": "512",
                #         "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                #         }
                # )
                # new_image_url =  output[1]


                deletion_confirm = delete_image_from_uploads(f'{user_email}.jpg')

                return jsonify({
                    'URL': 'new_image_url'
                })
        else:
            return charge_confirm


    else:
        return token_verification