from app.models.usuario import Usuario
from app.database import db

class UsuarioRepository:
    #salvando 
    @staticmethod
    def save(usuario: Usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    #buscando
    @staticmethod
    def chase_by_id(usuario_id: int):
        return Usuario.query.get(usuario_id)
    
    @staticmethod
    def chase_by_email(email:str):
        return Usuario.query.filter_by(email=email).first()
    
    @staticmethod
    def chase_by_cpf(cpf: int):
        return Usuario.query.filter_by(cpf=cpf).first()
    
    #mostrar
    @staticmethod
    def show():
        return Usuario.query.all()
    
    #atualizar
    @staticmethod
    def update():
        db.session.commit()

    #excluir *****
    @staticmethod
    def delete(usuario_id: int):
        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True