from flask import Blueprint, request, jsonify
from app.services.funcionario_service import RegisterServiceFuncionario
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity
from app.util.api_response import resposta_sucesso
from app.util.api_error import ApiError

funcionario_bp = Blueprint('funcionarios', __name__)

@funcionario_bp.route('/admin/register/funcionarios', methods=['POST'])
@perfil_required("GERENCIA", "ADMINISTRADOR", "GESTAO")
def register_funcionario():
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )     
    funcionario = RegisterServiceFuncionario.fucionarioRegister(dados)
    return resposta_sucesso(
        message="O funcionário foi cadastrado com sucesso.",
        data={
            "id": funcionario.id,
            "usuarioId": funcionario.usuario_id,
            "unidadeId": funcionario.unidade_id,
            "cargo": funcionario.cargo
        },
        status_code=200
    )

@funcionario_bp.patch('/admin/funcionarios/cargo/<int:funcionario_id>')
@perfil_required("GESTAO")
def alterar_cargo(funcionario_id):
    if funcionario_id is None:
        raise ApiError(
            error="FUNCIONARIO_NAO_ENCONTRADO",
            message="O funcionário informado não foi encontrado.",
            status_code=404,
            details=[{
                "field":"funcionarioId",
                "issue":f"O funcionário com Id {funcionario_id} não existe."
            }]
        )       
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )        
    funcionario = RegisterServiceFuncionario.alterar_cargo(funcionario_id, dados)
    return resposta_sucesso(
        message="O cargo do funcionário foi alterada com sucesso.",
        data={
            "funcionarioId": funcionario.id,
            "cargo": funcionario.cargo
        },
        status_code=200
    )

@funcionario_bp.patch('/admin/funcionarios/unidade/<int:funcionario_id>')
@perfil_required("GESTAO")
def alterar_unidade(funcionario_id):
    if funcionario_id is None:
        raise ApiError(
            error="FUNCIONARIO_NAO_ENCONTRADO",
            message="O funcionário informado não foi encontrado.",
            status_code=404,
            details=[{
                "field":"funcionarioId",
                "issue":f"O funcionário com Id {funcionario_id} não existe."
            }]
        )
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )    
    funcionario = RegisterServiceFuncionario.alterar_unidade(funcionario_id, dados)
    return resposta_sucesso(
        message="A unidade do funcionário foi alterada com sucesso.",
        data={
            "funcionarioId": funcionario.usuario_id,
            "unidadeId": funcionario.unidade_id
        },
        status_code=200
    )

@funcionario_bp.patch('/admin/funcionarios/<int:funcionario_id>/ferias/ativar')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def ativar_ferias(funcionario_id):
    if funcionario_id is None:
        raise ApiError(
            error="FUNCIONARIO_NAO_ENCONTRADO",
            message="O funcionário informado não foi encontrado.",
            status_code=404,
            details=[{
                "field":"funcionarioId",
                "issue":f"O funcionário com Id {funcionario_id} não existe."
            }]
        )
    RegisterServiceFuncionario.update_ferias(funcionario_id, True)
    return resposta_sucesso(
        message="O funcionário saiu de férias.",
        status_code=200
    )

@funcionario_bp.patch('/admin/funcionarios/<int:funcionario_id>/ferias/desativar')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def desativar_ferias(funcionario_id):
    if funcionario_id is None:
        raise ApiError(
            error="FUNCIONARIO_NAO_ENCONTRADO",
            message="O funcionário informado não foi encontrado.",
            status_code=404,
            details=[{
                "field":"funcionarioId",
                "issue":f"O funcionário com Id {funcionario_id} não existe."
            }]
        )
    RegisterServiceFuncionario.update_ferias(funcionario_id, False)
    return resposta_sucesso(
        message="O funcionário voltou de férias.",
        status_code=200
    )

@funcionario_bp.delete('/admin/funcionarios/<int:funcionario_id>/delete')
@perfil_required("GESTAO")
def delete_funcionario(funcionario_id):
    if funcionario_id is None:
        raise ApiError(
            error="FUNCIONARIO_NAO_ENCONTRADO",
            message="O funcionário informado não foi encontrado.",
            status_code=404,
            details=[{
                "field":"funcionarioId",
                "issue":f"O funcionário com Id {funcionario_id} não existe."
            }]
        )
    RegisterServiceFuncionario.deletar_funcionario(funcionario_id)
    return resposta_sucesso(
        message="O funcionário foi excluído com sucesso.",
        status_code=200
    ) 
  
