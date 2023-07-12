from flask import Flask
from handlers.userHandler import userRouter
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

PORT = os.getenv('PORT')

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(userRouter)

@app.route('/')
def index():
    return 'server running!'

if __name__ == '__main__':
    app.run(port=PORT)