from flask import Flask
from handlers.userHandler import userRouter
from dotenv import load_dotenv
import os
from flask_cors import CORS
from config import Config, DevelopmentConfig, ProductionConfig
from database import initialize
from handlers.paymentHandler import paymentRouter
from handlers.imagesHandler import imageRouter

load_dotenv()

PORT = os.getenv('PORT')

app = Flask(__name__)
cors = CORS(app)

env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
if env_config == "config.ProductionConfig":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

initialize()

app.register_blueprint(userRouter)
app.register_blueprint(paymentRouter)
app.register_blueprint(imageRouter)

@app.route('/')
def index():
    return 'server running!'