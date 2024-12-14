# # server/init_db.py
# import os
# from database import engine
# from models import Base

# # Check if the environment variable DROP_ALL_TABLES is set to "true"
# overwrite_tables = os.getenv("OVERWRITE_TABLES", "false").lower() == "true"

# if overwrite_tables:
#     # Drop all existing tables
#     print("Dropping all existing tables...")
#     Base.metadata.drop_all(bind=engine)

# # Create all tables
# print("Creating all tables...")
# Base.metadata.create_all(bind=engine)

# print("Database initialization complete.")
import os
from server.database import engine
from server.models import Base

# 如果需要重建表，可以设置环境变量 OVERWRITE_TABLES
overwrite_tables = os.getenv("OVERWRITE_TABLES", "false").lower() == "true"

if overwrite_tables:
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("Database initialization complete.")