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



@router.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = userCrud.get_users(db)
    return users

# @router.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = userCrud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@router.post("/users/")
def create_user(user: schemas.BaseUser, db: Session = Depends(get_db)):
    print(user.name)
    userCrud.create_user(db=db, user=user)    
    #db_user = crud.get_user_by_email(db, email=user.email)
    #if db_user:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return {'message':'employe créé'}


#Route to login in app
@router.post("/login")
async def user_login(loginitem:schemas.LoginItem, db: Session = Depends(get_db)):

    
    data = jsonable_encoder(loginitem)
    print(loginitem.email)
    print(data['email'])
    user = userCrud.get_user(db,data['email'])
    
    print(user)
    if user:
    # if data['email'] == user.email and user.check_password(data['password']):
        if user.check_password(data['password']):
            print('ok3')
            encoded_jwt = jwt.encode({'email': data['email'], 'exp': time() + ACCESS_TOKEN_EXPIRES}, Config.SECRET_KEY, algorithm=ALGORITHM)
            print(encoded_jwt)
            
            return {"token": encoded_jwt, "user" : user}

        else:
            return {"message":"login failed"}
    else:
        print('hello')

#Temporary route to fix my password, need to be modify to allow users change there passwords
@router.get("/pass/{user_id}")
def pass_user(user_id: int, db: Session = Depends(get_db)):
    print('hello')
    db_user = userCrud.get_user(db, user_id=user_id)
    db_user.set_password('fiction')
    db.commit()
    print(db_user)
    
    
    return print('ok')

#route to validate if token still valide
@router.post("/decode")
def token_decode(token :schemas.Decode, db: Session = Depends(get_db)):
    
    data = jsonable_encoder(token)
    print(data)
    
    
    
    if jwt.decode(token.token, Config.SECRET_KEY, algorithms=ALGORITHM)['email']:
        print('decode ok')
        print(jwt.decode(token.token, Config.SECRET_KEY, algorithms=ALGORITHM)['email'])
        
        return {"token": 'decode'}

    else:
        print('fail')
        return {"token":"decode failed"}
