from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.util.api_error import ApiError
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.pontos_repository import PontosRepository
from app.models.perfil import Perfil

class AuthServiceUsuario:

    @staticmethod
    def userRegister(dados):
        email_exists = UsuarioRepository.chase_by_email(dados['email'])
        cpf_exists = UsuarioRepository.chase_by_cpf(dados['cpf'])
        if email_exists:
            raise ApiError(
                error="EMAIL_JA_CADASTRADO",
                message="O email informado já foi cadastrado.",
                status_code=409,
                details=[]
            )   
        if cpf_exists:
            raise ApiError(
                error="CPF_JA_CADASTRADO",
                message="O cpf informado já foi cadastrado.",
                status_code=409,
                details=[]
            )      
        usuario = Usuario(
            nome = dados['nome'],
            email = dados['email'],
            cpf = dados['cpf'],
            telefone = dados['telefone'],
            cep = dados['cep'],
            senha_hash = generate_password_hash(dados['senha']),
            perfil = Perfil.CLIENTE
        )
        return UsuarioRepository.save(usuario)
    
    @staticmethod
    def login(user, senha):
        if '@' in user:
            usuario = UsuarioRepository.chase_by_email(user)
        else:
            usuario = UsuarioRepository.chase_by_cpf(user)
        if usuario is None:
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {user} não existe."
                }]
            ) 
        if not check_password_hash(usuario.senha_hash, senha):
            raise Exception("senha inválida")
        token = create_access_token(
            identity = str(usuario.id), 
            additional_claims={
                "perfil": usuario.perfil.value
            }
        )
        return token

    @staticmethod
    def atualizar(usuario_id, dados):
        usuario = UsuarioRepository.chase_by_id(usuario_id)
        if usuario is None:
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {usuario_id} não existe."
                }]
            )
        tipo = dados['dado'].upper()
        novo_valor = dados['novo_valor']
        if tipo == 'EMAIL':
            valor = UsuarioRepository.update_email(usuario_id, novo_valor)
        elif tipo == 'TELEFONE':
            valor = UsuarioRepository.update_tefefone(usuario_id, novo_valor)
        elif tipo == 'CEP':
            valor = UsuarioRepository.update_cep(usuario_id, novo_valor)
        elif tipo == 'SENHA':
            valor = UsuarioRepository.update_senha(usuario_id, novo_valor)
        else:
            raise ApiError(
                error="ALTERACAO_INVALIDA",
                message="Não é possível alterar este campo.",
                status_code=409,
                details=[{
                    "field":"tipoNovoValor",
                    "issue":"Apenas os campos 'EMAIL', 'TELEFONE', 'CEP, e 'SENHA', podem ser alteraddos."
                }]
            )   
        return valor

    @staticmethod
    def cadastro_ativo(usuario_id, bvalue):
        usuario = UsuarioRepository.chase_by_id(usuario_id)
        if usuario is None:
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {usuario_id} não existe."
                }]
            )
        nova_atualizacao = UsuarioRepository.update_activity(usuario.id, bvalue)
        return nova_atualizacao

    @staticmethod
    def delete_usuario(usuario_id):
        usuario = UsuarioRepository.chase_by_id(usuario_id)
        if usuario is None:
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {usuario_id} não existe."
                }]
            )
        return UsuarioRepository.delete(usuario.id)

