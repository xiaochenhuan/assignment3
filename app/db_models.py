from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


class HostStar(db.Model):
    __tablename__ = 'host_star'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(128), unique=True, nullable=False)
    sy_pnum = db.Column(db.Integer, nullable=True)
    sy_dist = db.Column(db.Float, nullable=True)
    sy_disterr1 = db.Column(db.Float, nullable=True)
    sy_disterr2 = db.Column(db.Float, nullable=True)
    # 反向引用 planets
    planets = db.relationship('Planet', backref='host_star', lazy=True)

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    pl_name = db.Column(db.String(128), nullable=False)
    discoverymethod = db.Column(db.String(64), nullable=True)
    disc_year = db.Column(db.Integer, nullable=True)
    disc_facility = db.Column(db.String(128), nullable=True)
    host_star_id = db.Column(db.Integer, db.ForeignKey('host_star.id'), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))