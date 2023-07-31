from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from flask_cors import CORS


app=None

def create_app():
    app=Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)

    CORS(app)
    db.init_app(app)
    app.app_context().push()
    
    db.create_all()
    app.app_context().push()

    return app

app=create_app()

from application.views import *

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8090)
