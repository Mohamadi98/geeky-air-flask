import jwt
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

def generate_token_for_email(email):
    # to set the expiry date of the token to 15 mins
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    expiry_timestamp = int(expiry.timestamp())
    user = {
        'email': email,
        'expiry': expiry_timestamp
        }
    token = jwt.encode(user, os.getenv('SECRET_TOKEN'), algorithm='HS256')

    return token