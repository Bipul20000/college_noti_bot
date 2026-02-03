from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# 1. Setup the SQLite Database connection
# This creates a file named 'notifications.db' in your folder
DATABASE_URL = "sqlite:///./notifications.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 2. Create the "Session" (this is like the handle to open the database drawer)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Define the structure (Schema)
Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # The headline of the notice
    link = Column(String, unique=True)  # The URL (must be unique so we don't save duplicates)
    date_posted = Column(String)        # The date string from the college site
    is_sent = Column(Boolean, default=False) # Have we sent this to Telegram yet?
    created_at = Column(DateTime, default=datetime.utcnow) # When did our bot find it?

# 4. Helper function to create the tables
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database created! 'notifications.db' file should appear.")

if __name__ == "__main__":
    # If we run this file directly, it builds the empty database
    init_db()