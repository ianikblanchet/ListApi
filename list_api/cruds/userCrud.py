from sqlalchemy.orm import Session
import models, schemas


def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_email: str):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    return user

def create_user(db: Session, user: schemas.BaseUser):
    #fake_hashed_password = user.password + "notreallyhashed"
    
    db_user = models.User(
                                           
                        name = user.name,
                        firstname = user.firstname,
                        employe_number = user.employe_number,
                        level = user.level,
                        email=user.email,                         
                        #password_hashd=fake_hashed_password,
                        )
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)    
    return db_user