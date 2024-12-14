# server/database.py
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session

# engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))

# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# 使用 SQLite 数据库
engine = create_engine("sqlite:///./test.db")

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

