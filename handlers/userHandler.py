from flask import Blueprint, request, jsonify
from models.user import user
from services.passwordHash import hashFunc
from services.checkDuplicates import check
from services.checkLoginCredentials import loginCredsCheck
from services.loginService import generateToken
from services.forgetPasswordService import forgetPass

userRouter = Blueprint('userHandler', __name__)

@userRouter.route('/signup', methods = ['POST'])
def signUp():
    request_data = request.get_json()

    if(check(request_data.get('email'), 'email') == True):
        return jsonify({'message': 'email already exists'}), 400
    
    if(check(request_data.get('username'), 'username')):
        return jsonify({'message': 'username already exists'}), 400
    
    if(check(request_data.get('password'), 'password')):
        return jsonify({'message': 'password already exists'}), 400

    user1 = user(username=request_data.get('username'),
                  email=request_data.get('email'),
                    password=hashFunc(request_data.get('password'))
                    )
    
    return user.create(user1)

@userRouter.route('/login', methods = ['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    result = loginCredsCheck(username, password)
    
    if result == False:
        return jsonify({'message': 'Invalid username or password'}), 400
    
    if result == 'admin':
        return jsonify({'message': 'admin user'}), 200
    
    return generateToken(username)

@userRouter.route('/forgetpassword', methods=['POST'])
def forgetPassword():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    
    return forgetPass(email, password)
