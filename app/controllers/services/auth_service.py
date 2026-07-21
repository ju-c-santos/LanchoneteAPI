from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

from app.repositories.usuario_repository import UsuarioRepository

class AuthServiceUsuario:
    
    @staticmethod
    def login(email, senha):
        usuario = UsuarioRepository.chase_by_email(email)
        if usuario is None:
            raise Exception("Usuário não encontrado")
        
        if not check_password_hash(usuario.senha_hash, senha):
            raise Exception("senha inválida")
        
        token = create_access_token(
            indentity = usuario.id, 
            additional_claims={
                "perfil": usuario.perfil
            }
        )

        return token