from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String,DateTime
import datetime
from flask_login import UserMixin



Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users' # テーブル名を明示的に指定
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(128))  # 本番ではハッシュ化してください (ハッシュ化されたパスワードは長くなるため、128文字程度を推奨)


class EntryExit(Base):
    __tablename__ = "entryexit"
    id = Column(Integer, primary_key=True)
    name =Column(String(50), nullable=False)
    action = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    def __repr__(self):
        return f'<EntryExit {self.name} {self.action} {self.timestamp}>'
