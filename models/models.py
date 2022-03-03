from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from db.database import Base, engine
from sqlalchemy import CheckConstraint

class BmiData(Base):
	'''
	This is database class. The name of the table is 'bmidatabase'. BmiDataORM
	it will have 6 attributes:
	1: name -> this will store the name of the user and will also act as primary key. type String
	2: age_yr -> this will store the age of the user in yrs and is of type Integer
	3: height_cm -> height of the user in cms and is of type Numeric and will contain number upto 2 decimal places.
	4: weight_kg -> weight of the user in kgs and is of type Numeric and will contain number upto 2 decimal places.
	5: bmi -> bmi of the user and is of type Numeric and will contain number upto 2 decimal places.
	6: last_updated -> will store the last date & time when bmi was updated
	''' 
	__tablename__ = "bmi_data"
	name = Column(String(20), primary_key=True, index=True)
	age_yr = Column(Integer, CheckConstraint('age_yr>12') , nullable = False)
	height_cm = Column(Numeric(4,2), CheckConstraint('age_yr>=152.40'),nullable = False)
	weight_kg = Column(Numeric(4,2), CheckConstraint('age_yr>=45.50'),nullable = False)
	bmi = Column(Numeric(3,2), nullable = False)
	last_updated = Column(String, nullable = False)

