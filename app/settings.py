import os
import redis
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# application instance
app = Flask(__name__)

# define working directory and path of settings.py
basedir = os.path.abspath(os.path.dirname(__file__))


# configuring the logging feature
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('./logs/errors.log', mode='a')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


# sql database variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
    os.path.join(basedir, '../db/library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SERVER_PORT"] = os.getenv("SERVER_PORT", "5000")
app.config["SERVER_IP"] = os.getenv("SERVER_IP", "0.0.0.0")


# JWT token variables
app.config["API_KEY"] = os.getenv("API_SECRET", "")
app.config["ALGORITHM"] = "HS256"
app.config["JWT_KEY"] = "&&<9[6,4}5Q@Avcn,;L@nOu[Jci6gdB:"


# database setup
db = SQLAlchemy(app)


# Redis Service controller
# set the default port and host values for redis server
# set the default db of redis to zero (0)
app.config["REDIS_DB"] = 0
app.config["REDIS_EXPIRY"] = 3600
redis_handler = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=app.config["REDIS_DB"]
)


@app.before_request
def initialize_db():
    """
    Initialize database file and commit the changes of all
    the defined tables or model structures
    """
    try:
        db.create_all()
    except Exception as e:
        logger.exception("[INIT DB] Error initializing database due to %s",
                         str(e), exc_info=True)
