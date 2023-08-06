import os
basedir=os.path.abspath(os.path.dirname(__file__))

SECRET_KEY="lachimolala"

class Config():
    SQLITE_DB_DIR=os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")
    DEBUG=True
    CACHE_TYPE= 'redis'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    CACHE_DEFAULT_TIMEOUT= 300
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

    

