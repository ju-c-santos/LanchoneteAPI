from app.models.perfil import Perfil
from app.models.funcionario import Funcionario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.util.api_error import ApiError

class RegisterServiceAdm:
    @staticmethod
    def admRegister(dados):
        cargo = dados['cargo'].upper()
        usuario = UsuarioRepository.chase_by_id(dados['usuario_id'])
        if usuario is None:
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {dados['usuario_id']} não existe."
                }]
            )
        if cargo not in ["ADMINISTRADOR", "GERENCIA"]:
            raise ApiError(
                error="ROTA_INVALIDA",
                message="Rota para cadastro inválida.",
                status_code=409,
                details=[{
                    "field":"cargo",
                    "issue":f"Apenas cargos de administração podem ser cadastrados aqui. (ADMINISTRADOR e GERENCIA)"
                }]
            )
        
        try:
            usuario.perfil = Perfil[cargo]
        except KeyError:
            raise ApiError(
                error="CARGO_INVALIDO",
                message="O cargo informado é inválido.",
                status_code=422,
                details=[{
                    "field":"cargo",
                    "issue":"Valores válidos: " + ", ".join(Perfil)
                }]
            )
        funcionario = Funcionario(
            usuario_id = dados['id'],
            unidade_id = dados['unidade'],
            cargo = cargo
        )
        return FuncionarioRepository.save(funcionario)
        