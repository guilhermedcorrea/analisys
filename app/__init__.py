from flask import Flask
import secrets
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from celery import Celery


from ..config import SQLALCHEMY_DATABASE_URI
from .extensions import db
from .make_celery import celery_init_app
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,),)
            
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = secrets.token_hex()
    app.config['SQLALCHEMY_POOL_SIZE'] = 370
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    app.config['MAX_CONTENT_LENGTH'] = 2 * 7024 * 7024
    app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.xlsx', '.xls']
    app.config['UPLOAD_PATH'] = r'/home/guilherme/analytics/app/uploads'
    app.config['DEBUG'] = True

    from .admin.Admin import Admin
   
    with app.app_context():
        db.init_app(app)
       
        migrate.init_app(app, db)
        app.register_blueprint(Admin)
        celery_init_app(app)
    return app