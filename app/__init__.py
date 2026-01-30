from app.routes import main
from flask import Flask, g
import os

from .db import SessionLocal,engine,route
from .models import Base



def init_db(app):

    # テーブル生成
    Base.metadata.create_all(bind=engine)

    @app.before_request
    def create_session():
        g.db = SessionLocal()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal.remove()


def create_app():

    app = Flask(__name__,
                static_folder=route.static,
                template_folder=route.templates)

    app.config["SQLALCHEMY_DATABASE_URI"] = route.database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # blueprint登録
    app.register_blueprint(main)

    init_db(app)

    return app
