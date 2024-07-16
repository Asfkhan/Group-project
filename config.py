import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','postgresql://aseef:dmABnCUras8QT6CgApZk4BtEXz1MQIGX@dpg-cqalhmggph6c73f61sc0-a:5432/asf')
    SECRET_KEY = os.getenv('SECRET_KEY', 'aseef_swati_parth_prakash_ninad')
