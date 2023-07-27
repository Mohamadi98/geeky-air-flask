from flask import Blueprint, request, jsonify
from models.user import user
from services.passwordHash import hashFunc
from services.checkDuplicates import check
from services.checkLoginCredentials import loginCredsCheck
from services.loginService import generateToken
from services.forgetPasswordService import forgetPass
from services.getUserInfoService import get_user_info

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
    username = request_data.get('email')
    password = request_data.get('password')
    result = loginCredsCheck(username, password)
    
    if result == False:
        return jsonify({'message': 'Invalid email or password'}), 400
    
    if result == 'admin':
        return jsonify({'message': 'admin user'}), 200
    
    return generateToken(username)

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

@userRouter.route('/sameh', methods = ['post'])
def sameh():
    request_data = request.get_json()
    image = request_data.get('image')
    print(image)
    data_type = type(image)
    return data_type
