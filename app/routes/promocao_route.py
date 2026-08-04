from flask import Blueprint, request, jsonify
from app.services.promocao_service import PromocaoService
from app.repositories.promocao_repository import PromocaoRepository
from app.util.decorator_perfil import perfil_required

promocao_bp = Blueprint('promocao', __name__)

@promocao_bp.route('/admin/promocoes/criar', methods=['POST'])
@perfil_required("ADMINISTRADOR")
def criar_promocao():
    try:
        dados = request.get_json()
        promocao = PromocaoService.create_promocao(dados)
        return jsonify({
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
        }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@promocao_bp.patch('/admin/promocoes/<int:promocao_id>/ativar')
@perfil_required('ADMINISTRADOR')
def ativar_promocao(promocao_id):
    try:
        PromocaoService.atividade(promocao_id, True)
        return jsonify ({
            "mensagem":"promoção ativa"
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 

@promocao_bp.patch('/admin/promocoes/<int:promocao_id>/desativar')
@perfil_required('ADMINISTRADOR')
def desativar_promocao(promocao_id):
    try:
        PromocaoService.atividade(promocao_id, False)
        return jsonify ({
            "mensagem":"promoção desativada"
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400     

@promocao_bp.get('/admin/promocoes')
@perfil_required("ADMINISTRADOR")
def listar_promocoes():
    try:
        registros = PromocaoRepository.listar_ativas()
        return jsonify([
            {
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
        ]), 200
    except Exception as e:
            return jsonify({"erro":str(e)}), 400 


@promocao_bp.delete('/admin/<int:pomocao_id>/delete')
@perfil_required("ADMINISTRADOR")
def delete_promocao(promocao_id):
    try:
        PromocaoService.delete_promocao(promocao_id)
        return jsonify({
            "mensagem": "Usuario excluído com sucesso."
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500      