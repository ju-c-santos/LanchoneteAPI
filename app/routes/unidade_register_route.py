from flask import Blueprint, request, jsonify
from app.services.unidade_service import ServiceUnidade
from app.util.decorator_perfil import perfil_required
from app.util.api_response import resposta_sucesso
from app.util.api_error import ApiError

unidade_bp = Blueprint('unidade', __name__)

@unidade_bp.route('/admin/register/unidade', methods=['POST'])
@perfil_required("GESTAO")
def unidade_register():
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        ) 
    unidade = ServiceUnidade.createUnidade(dados)
    return resposta_sucesso(
        message="A unidade foi registrada com sucesso.",
        data={
            "id": unidade.id,
            "cep": unidade.cep,
            "cidade": unidade.cidade,
            "estado": unidade.estado            
        },
        status_code=201
    )

@unidade_bp.patch('/admin/unidade/<int:unidade_id>/atualize/is_active/True')
@perfil_required("GESTAO")
def atividade_true(unidade_id):
    if unidade_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"unidadeId",
                "issue":f"A unidade com Id {unidade_id} não existe."
            }]
        )
    ServiceUnidade.alterar_atividade(unidade_id, True)
    return resposta_sucesso(
        message="Empresa agora se encontra em atividade.",
        status_code=200
    )

@unidade_bp.patch('/admin/unidade/<int:unidade_id>/atualize/is_active/False')
@perfil_required("GESTAO")
def atividade_false(unidade_id):
    if unidade_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"unidadeId",
                "issue":f"A unidade com Id {unidade_id} não existe."
            }]
        ) 
    ServiceUnidade.alterar_atividade(unidade_id, False)
    return resposta_sucesso(
        message="Empresa agora se encontra inativa.",
        status_code=200
    )

@unidade_bp.delete('/admin/unidade/<int:unidade_id>/delete')
@perfil_required("GESTAO")
def deletar_unidade(unidade_id):
    if unidade_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"unidadeId",
                "issue":f"A unidade com Id {unidade_id} não existe."
            }]
        )       
    ServiceUnidade.deletar_unidade(unidade_id)
    return resposta_sucesso(
        message="Unidade excluida com sucesso.",
        status_code=200
    )