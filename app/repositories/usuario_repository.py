from werkzeug.security import generate_password_hash
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

    @staticmethod
    def update_email(usuario_id:int, newEmail:str):
        usuario = Usuario.query.get(usuario_id)
        usuario.email = newEmail
        db.session.commit()
        return usuario

    @staticmethod
    def update_tefefone(usuario_id:int, newTel:str):
        usuario = Usuario.query.get(usuario_id)
        usuario.telefone = newTel
        db.session.commit()
        return usuario

    @staticmethod
    def update_cep(usuario_id:int, newCep:str):
        usuario = Usuario.query.get(usuario_id)
        usuario.cep = newCep
        db.session.commit()
        return usuario

    @staticmethod
    def update_senha(usuario_id:int, newSenha:str):
        usuario = Usuario.query.get(usuario_id)
        usuario.senha_hash = generate_password_hash(newSenha)
        db.session.commit()
        return usuario

    @staticmethod
    def update_perfil(usuario_id:int, newPerfil:str):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            raise ValueError("Usuário inexistente")
        usuario.perfil = newPerfil
        db.session.commit()
        return usuario

    @staticmethod  
    def update_activity(usuario_id, bolv):
        usuario = Usuario.query.get(usuario_id)
        usuario.cadastro_ativo = bolv
        db.session.commit()
        return usuario

    #excluir 
    @staticmethod
    def delete(usuario_id: int):
        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True