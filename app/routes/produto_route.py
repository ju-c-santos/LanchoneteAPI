from flask import Blueprint, request, jsonify
from app.services.produtos_service import ProdutoService
from app.repositories.historico_preco_repository import HistoricoPrecoRepository
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity


produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/admin/register/produto', methods=['POST'])
@perfil_required("GESTAO", "ADMINISTRADOR")
def add_produto():
    try:
        dados = request.get_json()
        produto = ProdutoService.novoProduto(dados)
        return jsonify({
            "id": produto.id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": produto.preco,
            "descricao": produto.descricao,
        }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

#ATERACAO DE PREÇO
@produto_bp.patch("/admin/produto/<int:produto_id>/valor")
@perfil_required("GESTAO")
def alterar_preco(produto_id):
    try:
        usuario_id = int(get_jwt_identity())
        dados = request.get_json()
        produto = ProdutoService.alterarValor(produto_id, usuario_id, dados)
        item = produto["produto"]
        return jsonify({
            "mensagem": "Preço atualizado em todas as unidades",
            "produto_id": item.id,
            "produto": item.nome,
            "novo_valor": float(item.preco),
            "estoques_atualizados": produto["estoques_atualizados"]
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 

#VISUALIZAR ALTERAÇÕES
@produto_bp.get('/funcionarios/precos/alteracoes')
@perfil_required("COZINHEIRO", "ATENDENTE", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def listar_alteracoes_preco():
    try:
        registros = HistoricoPrecoRepository.listar_recentes()
        return jsonify([
            {
                "id": registro.id,
                "produto_id": registro.produto_id,
                "produtos": registro.produtos.nome,
                "preco_anterior": float(registro.preco_anterior),
                "preco_novo": float(registro.preco_novo),
                "alterado_por": registro.usuario_id,
                "data_alteracao": registro.data_alteracao.isoformat()
            }
            for registro in registros
        ]), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 


@produto_bp.delete('/admin/<int:produto_id>/delete')
@perfil_required("GESTAO")
def delete_produto(produto_id):
    try:
        ProdutoService.delete_produto(produto_id)
        return jsonify({
            "mensagem": "Produto excluído com sucesso."
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500 

