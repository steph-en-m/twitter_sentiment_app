import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Tweepy Configurations
CONSUMER_KEY = "25O70MpmGuKOVn2z4q6Pnqg0g"
CONSUMER_SECRET = "RhsCbkW1IvqWywqXGeNl7zOzcfCFGBEnpx07Csk9lHLe0OXtdw"
ACCESS_TOKEN = "940556535222231040-YwDy453At4zZkZBKD1no1wLOSFbnXW4"
ACCESS_TOKEN_SECRET = "Z7vuvj4jauPJuy51MdHw8lc3HtGLh2df5bCsubjCQDsxB"


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "some key"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
