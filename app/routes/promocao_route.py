from flask import Blueprint, request, jsonify
from app.services.promocao_service import PromocaoService
from app.repositories.promocao_repository import PromocaoRepository
from app.util.decorator_perfil import perfil_required
from app.util.api_response import resposta_sucesso
from app.util.api_error import ApiError

promocao_bp = Blueprint('promocao', __name__)

@promocao_bp.route('/admin/promocoes/criar', methods=['POST'])
@perfil_required("GESTAO")
def criar_promocao():
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )
    promocao = PromocaoService.create_promocao(dados)
    return resposta_sucesso(
        message="A promoção foi criada com sucesso.",
        data={
            "id": promocao.id,
            "nome": promocao.nome,
            "produto_id": promocao.produto_id,
            "unidade_id": promocao.unidade_id,
            "tipo_desconto": promocao.tipo_desconto.value,
            "valor_desconto": float(promocao.valor_desconto),
            "quantidade_minima": promocao.quantidade_minima,
            "data_inicio": promocao.data_inicio.isoformat(),
            "data_fim": promocao.data_fim.isoformat(),
            "ativa": promocao.ativa            
        },
        status_code=201
    ) 

@promocao_bp.patch('/admin/promocoes/<int:promocao_id>/ativar')
@perfil_required("GESTAO")
def ativar_promocao(promocao_id):
    if promocao_id is None:
        raise ApiError(
            error="PROMOCAO_NAO_ENCONTRADA",
            message="A promoção informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"promocaoId",
                "issue":f"A promoção com o Id {promocao_id} não existe."
            }]
        )
    PromocaoService.atividade(promocao_id, True)
    return resposta_sucesso(
        message="A promoção foi ativada com sucesso.",
        status_code=200
    )

@promocao_bp.patch('/admin/promocoes/<int:promocao_id>/desativar')
@perfil_required("GESTAO")
def desativar_promocao(promocao_id):
    if promocao_id is None:
        raise ApiError(
            error="PROMOCAO_NAO_ENCONTRADA",
            message="A promoção informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"promocaoId",
                "issue":f"A promoção com o Id {promocao_id} não existe."
            }]
        )    
    PromocaoService.atividade(promocao_id, False)
    return resposta_sucesso(
        message="A promoção foi desativada com sucesso.",
        status_code=200
    )

@promocao_bp.get('/admin/promocoes')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def listar_promocoes():
    filtros={
        "promocao_id": request.args.get("promocaoId"),
        "nome_promocao": request.args.get("nomePromocao"),
        "produto_id": request.args.get("produtoId"),
        "tipo_promocao": request.args.get("tipoPromocao"),
        "data_inicio": request.args.get("dataInicio"),
        "data_fim": request.args.get("dataFim"),
        "valor_max": request.args.get("valorMax"),
        "valor_min": request.args.get("valorMin"),
        "ativa": request.args.get("ativa"),
        "ordenacao": request.args.get("ordenacao", default="promocaoId_asc"),
        "page": request.args.get("page", default=1, type=int),
        "limit": request.args.get("limit", default=20, type=int)
    }
    registros = PromocaoService.listar_promocao_filtrada(filtros)
    return resposta_sucesso(
        message="A lista de promoções foi consultada com sucesso.",
        data={{
                "id": promocao.id,
                "nome": promocao.nome,
                "produto_id": promocao.produto_id,
                "produto": promocao.produtos.nome,
                "unidade_id": promocao.unidade_id,
                "tipo_desconto": promocao.tipo_desconto.value,
                "valor_desconto": float(promocao.valor_desconto),
                "data_inicio": promocao.data_inicio.isoformat(),
                "data_fim": promocao.data_fim.isoformat()            
            }
            for promocao in registros
        },
        meta=registros["meta"],
        status_code=200
    )

@promocao_bp.delete('/admin/promocao/<int:promocao_id>/delete')
@perfil_required("GESTAO")
def delete_promocao(promocao_id):
    if promocao_id is None:
        raise ApiError(
            error="PROMOCAO_NAO_ENCONTRADA",
            message="A promoção informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"promocaoId",
                "issue": f"A promoção com o Id {promocao_id} não existe."
            }]
        )
    PromocaoService.delete_promocao(promocao_id)
    return resposta_sucesso(
        message="A promoção foi deletada com sucesso.",
        status_code=200
    ) 
