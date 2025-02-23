
from typing import List, Union, Optional
from datetime import date
from pydantic import BaseModel


    
class BaseUser(BaseModel):
    id : Optional[int]
    email : str
    name : str
    firstname : str
    password : str
    employe_number : Optional[str]
    level : str    
    

    class Config:
        orm_mode = True


class User(BaseUser):
    id : Optional[int]
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#class de mon ancien login    
class LoginItem(BaseModel):
    email: str
    password: str
    
#class de mon ancien login    
class Decode(BaseModel):
    token: str


class Categories(BaseModel):
    id : int
    name : str
    nom : str

    class Config:
        orm_mode = True

      
class Ing(BaseModel):
    id : int
    name : str
    categorie_id : int
    unite : str
    inventory : Optional[int]

    class Config:
        orm_mode = True


       
        