import os


class Config:
    DEBUG = os.environ.get("DEBUG")
    BACKEND_HOST = os.environ.get("BACKEND_HOST")
    BACKEND_PORT = os.environ.get("BACKEND_PORT")

    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = "shift_db" if int(os.environ.get("DOCKER")) else os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    if os.environ.get("ENV_MODE") == "production":
        SECRET_KEY = os.environ.get("SECRET_KEY")
