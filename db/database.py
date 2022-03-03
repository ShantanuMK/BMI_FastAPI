from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./BmiData.db" # determine read file paths  in python

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True} #most imp
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # read each meanings

Base = declarative_base()

'''
check_same-thread is used to restrict no of threads interacting with db at any given instance.
async def initializes only only one thread but def may initialize multiple threads so we have to explictly mention it
read in details
'''