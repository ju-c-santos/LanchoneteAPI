import os

class Config:
    SECRET_KEY = 'chave_admin'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lanchonete.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret'
