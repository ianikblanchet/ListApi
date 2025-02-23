from app import app, db ,login
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time

@login.user_loader
def load_user(id):
    return Benevole.query.get(int(id))

#declaration des models de table
class Liste(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    Prenom = db.Column(db.String(50), index = True)
    Nom = db.Column(db.String(50), index = True)
    Telephone = db.Column(db.String(12), index = True, unique = True)
    Telephone2 = db.Column(db.String(12), index = True)
    Heure = db.Column(db.String(5), index = True)
    Jour = db.Column(db.String(100), index = True)#une liste des jour abonnés
    langue = db.Column(db.String(12), index = True)
    Adresse = db.Column(db.String(50))
    Ville = db.Column(db.String(75), index = True)
    statut = db.Column(db.String(10), index = True, default='actif')
    contact_urg = db.Column(db.String(45), index = True)
    tel_urg1 = db.Column(db.String(20), index = True)
    tel_urg2 = db.Column(db.String(20), index = True)
    contact_urg2 = db.Column(db.String(45), index = True)
    tel_urg3 = db.Column(db.String(20), index = True)
    tel_urg4 = db.Column(db.String(20), index = True)
    date_inscr = db.Column(db.Date)
    Date_naissance = db.Column(db.Date)
    info_sup = db.Column(db.String(200), index = True)
    centre = db.Column(db.Integer, db.ForeignKey('centres.id'))
    cle = db.Column(db.Integer)
    urg1_cle = db.Column(db.Boolean)
    urg2_cle = db.Column(db.Boolean)


    Stats = db.relationship('StatAbon', backref='abonne', lazy='dynamic')
    Abs = db.relationship('Absences', backref='abonne', lazy='dynamic')
    def __repr__(self):
        return "{}  Nom: {} -- Tel : {}".format(self.id, self.Nom, self.Telephone)

class Benevole(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    Usager = db.Column(db.String(40), index = True)
    Prenom = db.Column(db.String(15), index = True)
    Nom = db.Column(db.String(15), index = True)
    Email = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))
    niveau = db.Column(db.String(20), default='attente')
    centre = db.Column(db.Integer, db.ForeignKey('centres.id'))
    Appel = db.relationship('StatAbon', backref='le_benevole', lazy='dynamic')

    def __repr__(self):
        return "{} -- {}".format(self.Usager, self.niveau)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Benevole.query.get(id)


class StatAbon(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    Date = db.Column(db.Date)
    Benevole = db.Column(db.Integer, db.ForeignKey('benevole.id'))
    Abonne = db.Column(db.Integer,  db.ForeignKey('liste.id'))
    Result_appel = db.Column(db.String(12), index = True)
    Alerte_etape = db.Column(db.String(15))
    Comment = db.Column(db.String(200))
    def __repr__(self):
        return "{}".format(self.id)

class Absences(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    date = db.Column(db.Date)
    Abonne = db.Column(db.Integer,  db.ForeignKey('liste.id'))

class Centres(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nom = db.Column(db.String(80))
    adresse = db.Column(db.String(80))
    ville = db.Column(db.String(80))
    direct = db.Column(db.String(75))
    tel = db.Column(db.String(12))
    benevole = db.relationship('Benevole', backref='centres', lazy='dynamic')
    abonne = db.relationship('Liste', backref='centres', lazy='dynamic')