from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

REFRESH_TOKEN_LIFETIME = 5
ACCESS_TOKEN_LIFETIME = 60
ALGORITHM = 'HS256'