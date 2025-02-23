from typing import Optional 
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import cruds.userCrud as userCrud
import models, schemas
from database import session
from sqlalchemy.orm import Session




def get_me():
    db = session
    try:
        yield db
    finally:
        db.close()

# Configuration du contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# URL pour obtenir le token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# Clé secrète pour signer les tokens JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": pwd_context.hash("secret"),
#         "disabled": False,
#     }
# }

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return User(**user_dict)

def authenticate_user(db, username: str, password: str):
    #user = userCrud.get_user(getattr(models.User, 'email') == username)
    user = userCrud.get_user(db, user_email = username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user( token: str = Depends(oauth2_scheme),db: Session = Depends(get_me)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    #user = userCrud.get_user(getattr(models.User, 'email') == token_data.username)
    user = userCrud.get_user(db = db, user_email = token_data.username)
    if user is None:
        raise credentials_exception
    return user