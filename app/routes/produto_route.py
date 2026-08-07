from flask import Blueprint, request, jsonify
from app.services.produtos_service import ProdutoService
from app.repositories.historico_preco_repository import HistoricoPrecoRepository
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity
from app.util.api_error import ApiError
from app.util.api_response import resposta_sucesso


produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/admin/register/produto', methods=['POST'])
@perfil_required("GESTAO", "ADMINISTRADOR")
def add_produto():
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )
    produto = ProdutoService.novoProduto(dados)
    return resposta_sucesso(
        message="Produto criado com sucesso!",
        status_code=201,
        data={
            "id": produto.id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": produto.preco,
            "descricao": produto.descricao,
            }
    )

#ATERACAO DE PREÇO
@produto_bp.patch("/admin/produto/<int:produto_id>/valor")
@perfil_required("GESTAO")
def alterar_preco(produto_id):
    usuario_id = int(get_jwt_identity())
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )
    if produto_id is None:
        raise ApiError(
            error="PRODUTO_NAO_ENCONTRADO",
            message="O produto informado não foi encontrado.",
            status_code=404,
            details=[{
                "field":"produtoId",
                "issue":f"O produto de Id {produto_id} não existe."
            }]
        )
    produto = ProdutoService.alterarValor(produto_id, usuario_id, dados)
    item = produto["produto"]
    return resposta_sucesso(
        message="Preço atualizado em todas a unidades com sucesso.",
        status_code=200,
        data={
            "mensagem": "Preço atualizado em todas as unidades",
            "produto_id": item.id,
            "produto": item.nome,
            "novo_valor": float(item.preco),
            "estoques_atualizados": produto["estoques_atualizados"]            
        }
    )


#VISUALIZAR ALTERAÇÕES
@produto_bp.get('/funcionarios/precos/alteracoes')
@perfil_required("COZINHEIRO", "ATENDENTE", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def listar_alteracoes_preco():
    filtros={
        "produto_id": request.args.get("produtoId"),
        "nome": request.args.get("nome"),
        "categoria": request.args.get("categoria"),
        "data_inicio": request.args.get("dataInicio"),
        "data_fim": request.args.get("dataFim"),
        "valor_novo_min": request.args.get("valorNovoMin"),
        "valor_novo_max": request.args.get("valorNovoMax"),
        "ordenar": request.args.get("ordenar", default="produtoId_desc"),
        "page": request.args.get("page", default=1, type=int),
        "limit": request.args.get("limit", default=20, type=int)
    }
    registros = ProdutoService.listar_preco_filtrado(filtros)
    return resposta_sucesso(
        message="Alterações de preço consultadas com sucesso.",
        data=registros["historico"],
        meta=registros["meta"],
        status_code=200
    )
