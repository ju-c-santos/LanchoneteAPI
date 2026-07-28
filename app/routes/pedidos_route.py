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