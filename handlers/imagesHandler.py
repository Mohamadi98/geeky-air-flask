from flask import Blueprint, request, jsonify
import replicate
from dotenv import load_dotenv
import os
from services.loginService import verifyToken, getUserFromToken
from services.chargeUserService import charge_user
from services.saveImageToUploads import save_base64_image, delete_image_from_uploads
from services.shopImageService import google_lens_request
from services.storeImageService import store_image

load_dotenv()

imageRouter = Blueprint('imageHandler', __name__)
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_KEY')

@imageRouter.route('/modify-image-upload', methods = ['POST'])
def modify_image_upload():
    request_data = request.get_json()
    if 'type' in request_data:
        room_type = request_data.get('type')

    else:
        room_type = ""

    if 'theme' in request_data:
        theme = request_data.get('theme')

    else:
        theme = ""

    token = request_data.get('token')
    image = request_data.get('image')

    token_verification = verifyToken(token)
    user_email = getUserFromToken(token)
    if user_email == 'admin@email.com':
        if len(image) < 200:
                # the image is a url
                output = replicate.run(
                    "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                    input={
                        "image": image,
                        "prompt": f'{theme} {room_type}',
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
            image_path_in_uploads = os.path.join('uploads', f'{user_email}.jpg')

            output = replicate.run(
                "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                input={
                    "image": open(image_path_in_uploads, 'rb'),
                    "prompt": f'{theme} {room_type}',
                    "num_samples": "1",
                    "image_resolution": "512",
                    "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                    }
            )
            new_image_url =  output[1]


            deletion_confirm = delete_image_from_uploads(f'{user_email}.jpg')

            return jsonify({
                'URL': new_image_url
            })




    if token_verification == True:
        charge_confirm = charge_user(token)
        if charge_confirm == True:
            if len(image) < 200:
                # the image is a url
                output = replicate.run(
                    "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                    input={
                        "image": image,
                        "prompt": f'{theme} {room_type}',
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
                image_path_in_uploads = os.path.join('uploads', f'{user_email}.jpg')

                output = replicate.run(
                    "jagilley/controlnet-hough:854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
                    input={
                        "image": open(image_path_in_uploads, 'rb'),
                        "prompt": f'{theme} {room_type}',
                        "num_samples": "1",
                        "image_resolution": "512",
                        "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
                        }
                )
                new_image_url =  output[1]


                deletion_confirm = delete_image_from_uploads(f'{user_email}.jpg')

                return jsonify({
                    'URL': new_image_url
                })
        else:
            return charge_confirm


    else:
        return token_verification
    
@imageRouter.route('/shop-modified-image', methods = ['POST'])
def shop_modified_image():
    request_data = request.get_json()
    token = request_data.get('token')
    image = request_data.get('image')
    token_verification = verifyToken(token)
    charge_confirm = charge_user(token)
    store_image_confirm = store_image(token, image)
    user_email = getUserFromToken(token)
    
    if store_image_confirm != True:
        return store_image_confirm
    
    if user_email == 'admin@email.com':
        return google_lens_request(image)
    
    if token_verification == True:
        if charge_confirm == True:
            return google_lens_request(image)
        
        else:
            return charge_confirm
    else:
        return token_verification

