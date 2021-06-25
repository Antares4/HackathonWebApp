from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def initapp(config_type=Config):
    app = Flask(__name__)
    app.config.from_object(config_type)
    db.init_app(app)
    with app.app_context():
        print("create database")
        db.create_all()
    from app.index import bp as index_bp
    app.register_blueprint(index_bp)

    return app

from app import model
