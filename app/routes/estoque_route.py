from flask import Blueprint, request, jsonify
from app.services.estoque_service import EstoqueService
from app.util.decorator_perfil import perfil_required

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/admin/add/estoque', methods=['POST'])
@perfil_required("GERENCIA", "ADMINISTRADOR")
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