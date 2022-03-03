import sys
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, FastAPI, dependencies
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud import crud_user
from db.database import engine, SessionLocal
from models import models
from exceptions.exceptions import UserAlreadyRegistered, UserNotFound

import schema.schema

models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


fake_users_db = {
    "shantanu": {
        "username": "shantanu",
        "full_name": "Shantanu Kardile",
        "email": "shantanu@example.com",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schema.User(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.post("/bmi/", response_model=schema.BmiUser)
def calculate_bmi(data: schema.BmiCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    obj = crud_user.add_user_to_db(data, db=db)
    if obj:
        return obj
    else:
        UserAlreadyRegistered()


@router.delete("/delete/{name}")
def delete_result(name: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if crud_user.delete_user_by_name(name, db=db):
        return {"response": "User Successfully deleted"}
    else:
        UserNotFound()


@router.post("/update/{name}", response_model=schema.BmiUser)
def update_bmi(name: str, data: schema.BmiUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    obj = crud_user.update_user_bmi(name, data, db=db)
    if obj:
        return obj
    else:
        UserNotFound()


@router.get("/read/", response_model=List[schema.BmiUser])
def read_bmi(name: Optional[str] = None, age: Optional[int] = None, page_size: int = Query(5, gt=0),
             page_number: int = Query(1, gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    filters = {"name": name, "age_yr": age}
    return crud_user.get_all_users(filters, (page_number - 1) * page_size, page_size, db=db)
