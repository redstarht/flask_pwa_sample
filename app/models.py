from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String,DateTime
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class EntryExit(Base):
    __tablename__ = "entryexit"
    id = Column(Integer, primary_key=True)
    name =Column(String(50), nullable=False)
    action = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    def __repr__(self):
        return f'<EntryExit {self.name} {self.action} {self.timestamp}>'
