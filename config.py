import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/erpdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
