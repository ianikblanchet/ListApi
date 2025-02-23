from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import Token, User, BaseUser
import main
from database import session
import logging

router = APIRouter()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()

@router.post("/api/v1/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logging.info(f"Received form data: {form_data.username}, {form_data.password}")
    user = authenticate_user(db , form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/usager/me")#, response_model=BaseUser)
async def read_users_me(current_user: BaseUser = Depends(get_current_user)):
    return current_user