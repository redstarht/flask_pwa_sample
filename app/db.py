from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .extensions import BuildDir
from .models import Base

# SQLAlchemy の初期化処理
engine = None
SessionLocal = None

route = BuildDir()
engine = create_engine(
    route.database_uri, connect_args={"check_same_thread": False}
)
SessionLocal = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


