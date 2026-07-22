from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.models.perfil import Perfil

class AuthServiceUsuario:

    @staticmethod
    def userRegister(dados):
        email_exists = UsuarioRepository.chase_by_email(dados['email'])
        cpf_exists = UsuarioRepository.chase_by_cpf(dados['cpf'])
        if email_exists:
            raise ValueError("E-mail já cadastrado.")
        if cpf_exists:
            raise ValueError("CPF já cadastrado")
        
        usuario = Usuario(
            nome = dados['nome'],
            email = dados['email'],
            cpf = dados['cpf'],
            telefone = dados['telefone'],
            senha_hash = generate_password_hash(dados['senha']),
            perfil = Perfil(dados['perfil'])
        )
        return UsuarioRepository.save(usuario)
    
    @staticmethod
    def login(user, senha):
        if '@' in user:
            usuario = UsuarioRepository.chase_by_email(user)
        else:
            usuario = UsuarioRepository.chase_by_cpf(user)

        if usuario is None:
            raise Exception("Usuário não encontrado")
        
        if not check_password_hash(usuario.senha_hash, senha):
            raise Exception("senha inválida")
        
        token = create_access_token(
            identity = str(usuario.id), 
            additional_claims={
                "perfil": usuario.perfil.value
            }
        )

        return token