import jwt
from dotenv import load_dotenv
import os
from flask import jsonify

load_dotenv()

def generateToken(username):
    # to set the expiry date of the token to 15 mins
    #expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    user = {'username': username}
    token = jwt.encode(user, os.getenv('SECRET_TOKEN'), algorithm='HS256')

    return jsonify({'token': token})

def verifyToken(token):
    try:
        secret_key = os.getenv('SECRET_KEY')
        # decode the token using the secret key and the HS256 algorithm
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        # extract the username from the payload
        username = payload["username"]

        # return the username
        return True
    except jwt.ExpiredSignatureError:
        # handle the case where the token has expired
        return jsonify({'message': 'token has expired'}), 400
    except jwt.InvalidTokenError:
        # handle the case where the token is invalid
        return jsonify({'message': 'invalid token'}), 400
    
def getUserFromToken(token):
    try:
        secret_key = os.getenv('SECRET_TOKEN')
        # decode the token using the secret key and the HS256 algorithm
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        username = payload["username"]

        return username
    except jwt.ExpiredSignatureError:
        # handle the case where the token has expired
        return jsonify({'message': 'token has expired'}), 400
    except jwt.InvalidTokenError:
        # handle the case where the token is invalid
        return jsonify({'message': 'invalid token'}), 400