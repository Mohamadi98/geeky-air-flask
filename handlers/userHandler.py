from flask import Blueprint, request, jsonify
from models.user import user
from services.passwordHash import hashFunc
from services.checkDuplicates import check
from services.checkLoginCredentials import loginCredsCheck
from services.loginService import generateToken
from services.forgetPasswordService import forgetPass
from services.getUserInfoService import get_user_info
import base64
from services.sendEmailService import send_email
from dotenv import load_dotenv
import os
from services.checkEmailExistService import check_email_exist
from services.tokenForEmailService import generate_token_for_email

load_dotenv()

userRouter = Blueprint('userHandler', __name__)

@userRouter.route('/signup', methods = ['POST'])
def signUp():
    request_data = request.get_json()

    if(check(request_data.get('email'), 'email') == True):
        return jsonify({'message': 'email already exists'}), 400
    
    if(check(request_data.get('username'), 'username') == True):
        return jsonify({'message': 'username already exists'}), 400

    user1 = user(username=request_data.get('username'),
                  email=request_data.get('email'),
                    password=hashFunc(request_data.get('password'))
                    )
    
    return user.create(user1)

@userRouter.route('/login', methods = ['POST'])
def login():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    result = loginCredsCheck(email, password)
    
    if result == False:
        return jsonify({'message': 'Invalid email or password'}), 400
    
    generated_token = generateToken(email)
    if result == 'admin':
        return jsonify({'message': 'admin user',
                        'token': generated_token
                        }), 200
    
    return jsonify({'token': generated_token})

@userRouter.route('/forgetpassword', methods=['POST'])
def forgetPassword():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    
    return forgetPass(email, password)

@userRouter.route('/user-info', methods=['POST'])
def user_info():
    request_data = request.get_json()
    token = request_data.get('token')

    return get_user_info(token)

@userRouter.route('/forget-password-mail', methods = ['POST'])
def send_mail_index():
    # app_password = os.getenv('MAIL_APP_PASSWORD')
    # return send_email(sender_email='mohamadinaena23@gmail.com', sender_password=app_password, recipient_email='essraabdalla2@gmail.com', subject='test', body='test message from python')
    request_data = request.get_json()
    email = request_data.get('email')
    result = check_email_exist(email)
    if result == True:
        email_token = generate_token_for_email(email)
        return jsonify({
            'URL': f'https://re-bamp.vercel.app/reset?token={email_token}'
        })

    else:
        return jsonify({
            'message': 'no user associated with this email'
        })
