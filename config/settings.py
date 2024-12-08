import os

class Config:
    SECRET_KEY = os.urandom(24)
    SESSION_COOKIE_NAME = 'myapp_session'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
