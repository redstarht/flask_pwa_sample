import os
from flask import Flask, g
from flask_login import LoginManager  
from datetime import timedelta

from .db import SessionLocal, engine, route
from .models import Base
from app.routes import main


login_manager = LoginManager()  


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

    app = Flask(__name__, static_folder=route.static, template_folder=route.templates)

    app.config["SQLALCHEMY_DATABASE_URI"] = route.database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(
        24
    )  # セッション管理に必須。本番では環境変数などから取得することを推奨
    # 有効期限を30日に設定する例
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)

    # Flask-Login設定の追加
    login_manager.init_app(app)
    login_manager.login_view = (
        "main.login"  # ログインが必要な場合のリダイレクト先をログインページに設定
    )
    login_manager.login_message = (
        "ログインが必要です。"  # ログインが必要な場合に表示されるメッセージ
    )
    login_manager.login_message_category = "info"  # メッセージのカテゴリ

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        session = (
            SessionLocal()
        )  # リクエストコンテキスト外でも呼ばれる可能性があるため、新しいセッションを作成
        user = session.query(User).get(int(user_id))
        session.close()  # セッションを閉じる
        return user

    # blueprint登録
    app.register_blueprint(main)

    # PWA Service Worker ルート設定の追加
    @app.route("/sw.js")
    def sw():
        return app.send_static_file("sw.js")

    init_db(app)

    return app
