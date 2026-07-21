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
        return Usuario.query.filter_by(email=email).firts()
    
    #mostrar
    @staticmethod
    def show():
        return Usuario.query.all()
    
    #atualizar
    @staticmethod
    def update():
        db.session.commit()

    #excluir
    @staticmethod
    def delete(usuario: Usuario):
        db.session.delete(usuario)
        db.session.commit()