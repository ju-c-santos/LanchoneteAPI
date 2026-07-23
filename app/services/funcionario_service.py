from app.models.perfil import Perfil
from app.models.funcionario import Funcionario
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

        if funcionario.cargo == Perfil.GERENCIA:
            usuario.perfil = Perfil.GERENCIA

        elif funcionario.cargo == Perfil.ADMINISTRADOR:
            usuario.perfil = Perfil.ADMINISTRADOR

        elif funcionario.cargo == Perfil.COZINHEIRO:
            usuario.perfil = Perfil.COZINHEIRO
        else:
            usuario.perfil = Perfil.ATENDENTE

        return FuncionarioRepository.save(funcionario)
