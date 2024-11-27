import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'username'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'hp_db'