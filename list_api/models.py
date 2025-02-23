from sqlalchemy import Column, Integer, String , Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
from datetime import date
from sqlalchemy.dialects.postgresql import JSONB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from config import Config 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), index=True, unique=True)
    name = Column(String(32), index=True)
    firstname = Column(String(32), index=True)
    employe_number = Column(String(15), index=True)
    level = Column(String(64), index=True) 
    

    password_hash = Column(String(128))
    
    

    def __repr__(self):
        return 'username={} {} {}'.format(self.employe_number, self.name, self.firstname  )
    
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    def set_password(self, password:str):
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            Config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True)
    nom = Column(String(32), index=True)
    ingredient = relationship('Ingredient', backref = 'categories', lazy = 'joined')   



class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)    
    name = Column(String(32), index=True)
    categorie_id = Column(Integer, ForeignKey('categories.id'))
    unite = Column(String(32), index=True)
    inventory = Column(Integer)   
    


     
    

#Base.metadata.create_all(engine)