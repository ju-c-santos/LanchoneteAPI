from flask import Blueprint, request, jsonify
from app.services.estoque_service import EstoqueService
from app.repositories.unidade_repository import UnidadeRepository
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/admin/atualize/estoque', methods=['POST'])
@perfil_required("GERENCIA", "ADMINISTRADOR", "GESTAO")
def add_to_estoque():
    try:
        dados = request.get_json()
        estoque = EstoqueService.addProduto(dados)
        return jsonify({
            "id_produto": estoque.id_produto,
            "id_unidade": estoque.id_unidade,
            "quantidade": estoque.quantidade,
            "preco": estoque.preco,
            "categoria": estoque.categoria
        }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@estoque_bp.patch('/admin/atualize/is_active/<int:estoque_id>')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def atualizar_disponibilidade(estoque_id):
    try:
        usuario_logado = int(get_jwt_identity())
        produto = EstoqueService.alterar_disponibilidade(usuario_logado, estoque_id)
        return jsonify({
            "id_produto": produto.id_produto,
            "is_active": produto.is_active
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@estoque_bp.patch('/admin/estoque/<int:estoque_id>/quantidade')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def atualizar_quantidade_estoque(estoque_id):
    try:
        dados = request.get_json()
        estoque = EstoqueService.somar_quantidade(estoque_id, dados)
        return jsonify({
            "mensagem": "Quantidade atualizada com sucesso",
            "estoque_id": estoque.id,
            "produto_id": estoque.id_produto,
            "unidade_id": estoque.id_unidade,
            "quantidade": estoque.quantidade,
            "is_active": estoque.is_active
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400
    

@estoque_bp.get('/unidade/<int:unidade_id>/menu')
def visualizar_menu(unidade_id):
    try:
        unidade = UnidadeRepository.chase_by_id(unidade_id)
        if unidade is None:
            raise ValueError("Unidade inválida")
        menu = EstoqueService.menu_cliente(unidade_id)
        return jsonify({
            "unidade": {
                "id": unidade.id,
                "endereco": unidade.endereco,
                "estado": unidade.estado 
            },
            "quatidade_produtos": len(menu),
            "produtos": menu
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500