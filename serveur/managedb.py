
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, UniqueConstraint,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class scan(Base):
    __tablename__ = 'scan'
    id = Column(Integer, primary_key=True, index=True)
    scanid = Column(String, index=True)
    file_path = Column(String)
    scandate = Column(DateTime)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()