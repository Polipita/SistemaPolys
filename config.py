from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'mysql+pymysql://root:@localhost/saas_veterinaria_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'el-secreto-local'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)