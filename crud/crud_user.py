# all crud functions
import datetime
from sqlalchemy.orm import Session
import schema.schema
from exceptions.exceptions import UserAlreadyRegistered, PageNotFound
from models import BmiData


def get_user_by_name(name, db: Session) -> bool:
    '''
	this func allows us to check/ validate if user is present in database or not.
	:para name -> name of the user to validate
	:type name -> string
	'''
    present = db.query(BmiData).filter(BmiData.name == name).first()
    print(present)
    if present:
        print(present.name, present.age_yr, present.height_cm)
        return True
    return False


def add_user_to_db(data, db: Session):
    '''
	this function add the user to database with his name, age, height, weight, and his bmi
	'''
    bmi = calculate_bmi(data.height_cm, data.weight_kg)
    category = bmi_category(bmi)
    date = str(datetime.datetime.now().replace(microsecond=0))
    bmidata = BmiData()  # args & kwarqs in py
    bmidata.name = data.name
    bmidata.age_yr = data.age_yr
    bmidata.height_cm = data.height_cm
    bmidata.weight_kg = data.weight_kg
    bmidata.bmi = bmi
    bmidata.last_updated = date
    try:
        db.add(bmidata)
        db.commit()
    except Exception as e:
        raise UserAlreadyRegistered()

    # comment = "Hi {} You are {} years old with a height of {} cm and your BMI is {}. Scientifically, you're in the {} category.".format(data.name, data.age_yr, data.height_cm, bmi, category)
    return bmidata


def delete_user_by_name(name, db: Session):
    '''
	function to delete the user from database
	'''
    try:
        db.query(BmiData).filter(BmiData.name == name).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)


def update_user_bmi(name, data: schema.BmiUpdate, db: Session):
    obj = db.query(BmiData).filter(BmiData.name == name).first()
    if obj:
        if data.age_yr:
            obj.age_yr = data.age_yr
        if data.height_cm or data.weight_kg:
            updated_height = data.height_cm if data.height_cm else obj.height_cm
            updated_weight = data.weight_kg if data.weight_kg else obj.weight_kg
            obj.bmi = calculate_bmi(updated_height, updated_weight)
            obj.height_cm = updated_height
            obj.weight_kg = updated_weight

        date = str(datetime.datetime.now().replace(microsecond=0))
        obj.last_updated = date
        db.add(obj)
        db.commit()  # db.refresh(obj)
        return obj
    else:
        return False


def get_all_users(filters, skip, limit, db: Session):
    query = db.query(BmiData)
    print(filters)
    for key, value in filters.items():
        if value != None:
            query = query.filter(getattr(BmiData, key) == value)
    results = query.offset(skip).limit(limit).all()
    if results:
        return results
    else:
        PageNotFound()


def calculate_bmi(height: float, weight: float):
    '''
	This function calculates the bmi value and return bmi and height(in cms).
	
	:para weight : this is user's weight
	:type weight : float
	:para age : age of the user.
	:type age : int
	:para height : height(cms) of the user
	:type height : float
	'''
    weight = round(weight, 2)
    bmi = (float(weight * 10000) / float(height ** 2))
    return round(bmi, 2)


def bmi_category(bmi):
    '''
	This function decides the category based on the given bmi value.
	:para bmi: This value is used to decide the bmi category
	:type bmi: float
	'''
    category = ""
    if bmi < 18.5:
        category = "Underweight"
    elif (18.5 <= bmi <= 24.9):
        category = "Healthy-Weight"
    elif (25.0 <= bmi <= 29.9):
        category = "Overweight"
    else:
        category = "Obese"

    return category


'''
1: mock

git-repo -> mac -> dryrun
'''
