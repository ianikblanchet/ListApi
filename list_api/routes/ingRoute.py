from typing import List
import jwt
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from config import Config
from time import time
import models
import json
import cruds.userCrud as userCrud
import cruds.ingCrud as ingCrud
import schemas
from database import session


router = APIRouter()

ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRES = 600




# Dependency
def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()



@router.get("/ings/", response_model=List[schemas.Ing])
def read_ings(db: Session = Depends(get_db)):
    ings= ingCrud.get_ings(db) 
    return ings