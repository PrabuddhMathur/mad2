from flask import Flask
from application.config import Config, SECRET_KEY
from passlib.hash import pbkdf2_sha256 as passhash
from application.database import db
from application.models import *
from flask_cors import CORS
from application import workers
import secrets

app=None

def create_app():
    app=Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.secret_key=SECRET_KEY
    db.init_app(app)
    app.app_context().push()
    
    db.create_all()

    admin_user = User.query.filter_by(isadmin=1).first()
    if not admin_user:
        email='admin@admin.com'
        username = 'admin'
        password = '1234'
        admin_user=User(email=email, username=username,password=passhash.hash(password),isadmin=1)
        db.session.add(admin_user)
        db.session.flush()
        db.session.refresh(admin_user)

        token = Token(user_id=admin_user.id, token=secrets.token_urlsafe(32))

        db.session.add(token)
        db.session.commit()

    app.app_context().push()

    # Initialize Celery
    celery = workers.celery
    # celery.conf.enable_utc=False
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        # timezone=app.config["CELERY_TIMEZONE"],
    )
    # celery.conf.beat_schedule()
    celery.Task = workers.ContextTask
    app.app_context().push()
    return app, celery

app, celery = create_app()

from application.views import *

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8090)
