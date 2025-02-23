from sqlalchemy.orm import Session
import models, schemas


def get_ings(db: Session):
    return db.query(models.Ingredient).join(models.Categories).all()


def create_ing(db: Session, ing: schemas.Ing):
    
    
    db_ing = models.Ingredient(
                                           
                        name = ing.name,
                        categorie_id  = ing.categorie_id,                        
                        unite = ing.unite,
                        inventory= ing.inventory,                    
                        
                        )
   
    db.add(db_ing)
    db.commit()
    db.refresh(db_ing)    
    return db_ing
 
def create_cat(db: Session, cat: schemas.Categories):
    
    
    db_cat = models.Categories(
                                           
                        name = cat.name,
                        nom  = cat.nom, 
                        )
   
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)    
    return db_cat