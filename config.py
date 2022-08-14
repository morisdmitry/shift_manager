import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.environ.get("DEBUG")
    BACKEND_HOST = os.environ.get("BACKEND_HOST")
    BACKEND_PORT = os.environ.get("BACKEND_PORT")

    # connect to postgresql
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = "shift_db" if int(os.environ.get("DOCKER")) else os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # connect to mailgun
    MG_API = os.environ.get("MG_API")
    MG_LINK = os.environ.get("MG_LINK")
    MG_MAIL = os.environ.get("MG_MAIL")
    MG_RECIPIENTS = os.environ.get("MG_RECIPIENTS")

    # connect to AWS
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = os.environ.get("S3_BUCKET")

    if os.environ.get("ENV_MODE") == "production":
        SECRET_KEY = os.environ.get("SECRET_KEY")
