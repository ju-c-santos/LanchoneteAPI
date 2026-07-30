from flask import Blueprint, request, jsonify
from app.services.produtos_service import ProdutoService
from app.util.decorator_perfil import perfil_required

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/admin/register/produto', methods=['POST'])
@perfil_required("GERENCIA", "ADMINISTRADOR")
def add_produto():
    try:
        dados = request.get_json()
        produto = ProdutoService.novoProduto(dados)
        return jsonify({
            "id": produto.id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": produto.preco,
            "descricao": produto.descricao
        }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500