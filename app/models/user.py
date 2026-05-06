from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))

    def set_password(self, senha):
        self.password = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.password, senha)