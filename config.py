import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'aseef_swati_parth_prakash_ninad')
