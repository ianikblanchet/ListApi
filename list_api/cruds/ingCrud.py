from sqlalchemy.orm import Session
import models, schemas


def get_ings(db: Session):
    return db.query(models.Ingredient).join(models.Categories).all()