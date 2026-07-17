from app.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(150), unique = False)
    senha_hash = db.Column(db.String(225))