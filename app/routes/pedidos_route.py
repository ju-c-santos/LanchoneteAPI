from flask import Blueprint, request, jsonify
from app.services.pedido_service import PedidoService
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity

pedido_bp = Blueprint("pedido", __name__)

@pedido_bp.route("/login/pedidos", methods=['POST'])
@perfil_required('CLIENTE')
def criar_pedido():
    try:
        usuario_id = get_jwt_identity()
        dados = request.get_json()
        pedido = PedidoService.criar_pedido(usuario_id, dados)
        return jsonify (pedido.to_dict()), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


#ROTAS PARA ALTERAÇÃO DE STATUS
@pedido_bp.patch("/<int:id>/status/aceitar")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR")
def aceitar_pedido(id):
    try:
        PedidoService.preparar_pedido(id)
        return jsonify({"msg":"Pedido em preparo"}), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@pedido_bp.patch("/<int:id>/status/pronto")
@perfil_required("COZINHEIRO", "GERENCIA", "ADMINISTRADOR")
def pedido_pronto(id):
    try:
        PedidoService.pedido_pronto(id)
        return jsonify({"msg":"Pedido pronto"}), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@pedido_bp.patch("/<int:id>/status/entrega")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR")
def pedido_entrega(id):
    try:
        PedidoService.aguardando_entregador(id)
        return jsonify({"msg":"Aguardando entregador"}), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@pedido_bp.patch("/<int:id>/status/finalizar")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR")
def finalizar(id):
    try:
        usuario_id = get_jwt_identity()
        PedidoService.finalizar(id)
        return jsonify({"msg":"Pedido Finalizado"}), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@pedido_bp.patch("/<int:id>/status/cancelar")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR")
def cancelar(id):
    try:
        PedidoService.cancelar(id)
        return jsonify({"msg":"Pedido cancelado"}), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400