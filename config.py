import os


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get("SK")
    NAME_DB = os.environ.get("DB_NAME")
    USER = os.environ.get("DB_USER")
    PASSWORD = os.environ.get("PASSWORD")

    # host for connect to docker-compose db
    HOST = 'postgres_db'
    
    # switch hosts for connect to local or remote db
    # HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    BACKEND_PORT = os.environ.get("BACKEND_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME_DB}"
