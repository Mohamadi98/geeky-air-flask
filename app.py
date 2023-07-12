from flask import Flask
from handlers.userHandler import userRouter
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(userRouter)

@app.route('/')
def index():
    return 'server running!'