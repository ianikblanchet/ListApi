from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config



#connection with bd
Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
#session.close_all()





