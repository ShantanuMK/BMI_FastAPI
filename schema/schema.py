from typing import Optional
from pydantic import BaseModel, Field, validators, validator


class BmiBase(BaseModel):
	
	age_yr : int #= Field(ge=13, description="Age should be greater than 13yrs")
	weight_kg : float #= Field(ge=45.50, description="Values should be in kgs & Minimum weight should be 45.5kgs")
	height_cm : float #= Field(ge=152.40, description="Age should be in cms and greater than 152.40 cms")

	@validator('age_yr', pre = True, always = True) #always: 
	def check_age(cls, value):
		if value is not None and value < 13:
			raise ValueError('Age should be greater than 12yrs')
		return value


	@validator('height_cm', pre = True, always = True)
	def check_height(cls, value):
		if value is not None and value < 150.40:
			raise ValueError('Height should be greater than 152.40 cms')
		return value

	@validator('weight_kg', pre = True, always = True)
	def check_weight(cls, value):
		if value is not None and value < 45.50:
			raise ValueError('Weight should be greater than 45.50 kg')
		return value


class BmiUpdate(BmiBase):
	age_yr : Optional[int] = None #(check_age(age_yr))#pydantic validators -> func writte in base class and implemented here.
	weight_kg : Optional[float] = None #(check_weight(weight_kg))
	height_cm : Optional[float] = None #check_height(height_cm)


class BmiCreate(BmiBase):
	name : str = Field(max_length=20, min_length=1, regex='[a-zA-Z.]')


class BmiUser(BmiCreate):
	bmi : float
	last_updated : str
	class Config:
		orm_mode = True #fetching obj and converting to pydantic model


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str


    

