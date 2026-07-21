from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository

class AuthServiceUsuario:

    @staticmethod
    def userRegister(dados):
        usuario_exists = UsuarioRepository.chase_by_email(dados['email'])
        if usuario_exists:
            raise ValueError("E-mail já cadastrado.")
        
        usuario = Usuario(
            nome = dados['nome'],
            email = dados['email'],
            senha_hash = generate_password_hash(dados['senha'])
        )
        return UsuarioRepository.save(usuario)
    
    @staticmethod
    def login(email, senha):
        usuario = UsuarioRepository.chase_by_email(email)
        if usuario is None:
            raise Exception("Usuário não encontrado")
        
        if not check_password_hash(usuario.senha_hash, senha):
            raise Exception("senha inválida")
        
        token = create_access_token(
            identity = usuario.id, 
            additional_claims={
                "perfil": usuario.perfil
            }
        )

        return token