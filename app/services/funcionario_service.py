from app.models.perfil import Perfil
from app.models.funcionario import Funcionario
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.funcionario_repository import FuncionarioRepository

class RegisterServiceFuncionario:
    @staticmethod
    def fucionarioRegister(dados):

        usuario = UsuarioRepository.chase_by_id(dados['id'])
        if usuario is None:
            raise ValueError("Usuario não encontrado")


        funcionario = Funcionario(
            usuario_id = dados['id'],
            unidade_id = dados['unidade'],
            cargo = dados['cargo']
        )

        usuario.perfil = Perfil.FUNCIONARIO

        return FuncionarioRepository.save(funcionario)
