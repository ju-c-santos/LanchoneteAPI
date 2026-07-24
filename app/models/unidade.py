from app.database import db

class Unidade(db.Model):
    __tablename__ = 'unidade'

    id = db.Column(db.Integer, primary_key= True)
    endereco = db.Column(db.String(150), nullable = False)
    bairro = db.Column(db.String(150), nullable = False)
    cep = db.Column(db.String(9), nullable= False)
    cidade = db.Column(db.String(50), nullable = False)
    estado = db.Column(db.String(2), nullable = False)

    funcionarios = db.relationship(
        "Funcionario", 
        back_populates = "unidade",
        #relacionamento 1 - 1.. -> uselist = True
        )
    
    