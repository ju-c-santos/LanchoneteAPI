from flask import Blueprint, request, jsonify
from app.services.estoque_service import EstoqueService
from app.repositories.unidade_repository import UnidadeRepository
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity
from app.util.api_error import ApiError
from app.util.api_response import resposta_sucesso

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/admin/estoque', methods=['POST'])
@perfil_required("GERENCIA", "ADMINISTRADOR", "GESTAO")
def add_to_estoque():
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )
    estoque = EstoqueService.addProduto(dados)
    return resposta_sucesso(
        message="Item adicionado ao estoque com sucesso!",
        status_code=201,
        data={
            "id_produto": estoque.id_produto,
            "id_unidade": estoque.id_unidade,
            "quantidade": estoque.quantidade,
            "preco": estoque.preco,
            "categoria": estoque.categoria
        }
    )
 
@estoque_bp.patch('/admin/estoque/produtos/<int:estoque_id>/disponivel/true')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def atualizar_disponibilidade_true(estoque_id):
    usuario_logado = int(get_jwt_identity())
    if estoque_id is None:
        raise ApiError (
            error="ESTOQUE_NAO_ENCONTRADO",
            message="O estoque informado não foi encontrado.",
            status_code=404,
            details=[{
                "fields":"estoqueId",
                "issue":f"O estoque {estoque_id} não foi encontrado."
            }]
        )
    produto = EstoqueService.alterar_disponibilidade(usuario_logado, estoque_id, True)
    return resposta_sucesso(
        message="O item está disponível.",
        status_code=200,
        data={
            "id_produto": produto.id_produto,
            "is_active": produto.is_active
        }
    )

@estoque_bp.patch('/admin/estoque/produtos/<int:estoque_id>/disponivel/false')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def atualizar_disponibilidade_false(estoque_id):
    usuario_logado = int(get_jwt_identity())
    if estoque_id is None:
        raise ApiError (
            error="ESTOQUE_NAO_ENCONTRADO",
            message="O estoque informado não foi encontrado.",
            status_code=404,
            details=[{
                "fields":"estoqueId",
                "issue":f"O estoque {estoque_id} não foi encontrado."
            }]
        )
    produto = EstoqueService.alterar_disponibilidade(usuario_logado, estoque_id, False)
    return resposta_sucesso(
        message="O item não está mais disponível.",
        status_code=200,
        data={
            "id_produto": produto.id_produto,
            "is_active": produto.is_active
        }
    )

@estoque_bp.patch('/admin/estoque/<int:estoque_id>/quantidade')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def atualizar_quantidade_estoque(estoque_id):
    if estoque_id is None:
        raise ApiError (
            error="ESTOQUE_NAO_ENCONTRADO",
            message="O estoque informado não foi encontrado.",
            status_code=404,
            details=[{
                "fields":"estoqueId",
                "issue":f"O estoque {estoque_id} não foi encontrado."
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
    estoque = EstoqueService.somar_quantidade(estoque_id, dados)
    return resposta_sucesso(
        message="Quantidade em estoque atualizada com sucesso.",
        status_code=200,
        data={
            "mensagem": "Quantidade atualizada com sucesso",
            "estoque_id": estoque.id,
            "produto_id": estoque.id_produto,
            "unidade_id": estoque.id_unidade,
            "quantidade": estoque.quantidade,
            "is_active": estoque.is_active
        }
    )

@estoque_bp.get('/unidade/<int:unidade_id>/menu')
def visualizar_menu(unidade_id):
    unidade = UnidadeRepository.chase_by_id(unidade_id)
    if unidade is None:
        raise ApiError(
            error = "UNIDADE_NAO_ENCONTRADA",
            message = "A unidade informada não foi encontrada.",
            status_code = 404,
            details = [{
                    "fields":"unidadeId",
                    "issue": (f"Não existe unidade de ID {unidade_id}")
                }
            ]
        )
    filtros = {
        "nome": request.args.get("nome"),
        "categoria": request.args.get("categoria"),
        "disponivel": request.args.get("disponivel"),
        "preco_min": request.args.get("precoMin"),
        "preco_max": request.args.get("precoMax"),
        "ordernar": request.args.get("ordenar", default="nome_asc"),
        "page": request.args.get("page", default=1, type=int),
        "limit": request.args.get("limit", default=20, type=int)
    }
    menu = EstoqueService.menu_cliente(unidade_id, filtros)
    return resposta_sucesso(
        message="Cardápio consultado com sucesso.",
        status_code=200,
        data={
            "unidade": {
                "id": unidade.id,
                "endereco": unidade.endereco,
                "estado": unidade.estado 
            },
            "produtos": menu["produtos"]
        },
        meta={
            "page": menu["page"],
            "limit": menu["limit"],
            "totalItems": menu["totalItems"],
            "totalPages": menu["totalPages"],
            "hasNext": menu["hasNext"],
            "hasPrevious": menu["hasPrevious"]           
        }
    )