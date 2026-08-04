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


@pedido_bp.patch("/pedidos/<int:pedido_id>/itens/<int:item_id>")
@perfil_required("CLIENTE")
def alterar_item_pedido(pedido_id, item_id):
    try:
        usuario_id = int(get_jwt_identity())
        dados = request.get_json
        pedido = PedidoService.alterar_item(pedido_id, item_id, usuario_id, dados)
        return jsonify ({
            "mensagem":"Item alterado com sucesso",
            "pedido":pedido.to_dict()
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500

#ROTAS PARA RETORNO
#para o usuario
@pedido_bp.get('/login/pedidos/historico')
@perfil_required('CLIENTE')
def historico_cliente():
    try:
        usuario_id = int(get_jwt_identity())
        pedidos = PedidoService.historico_pedidos_all(usuario_id)
        return jsonify({
            "quantidade": len(pedidos),
            "pedidos": pedidos
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500    


#rota para administradores
@pedido_bp.get('/admin/pedidos/historico/<int:usuario_id>')
@perfil_required('ADMINISTRADOR', 'GERENCIA')
def historico_cliente_adm(usuario_id):
    try:
        pedidos = PedidoService.historico_pedidos_all(usuario_id)
        return jsonify({
            "quantidade": len(pedidos),
            "pedidos": pedidos
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500    

#listagem de pedidos do dia atual
@pedido_bp.get('/admin/pedidos')
@perfil_required('ADMINISTRADOR', 'GERENCIA')
def pedidos_hoje():
    try:
        usuario_id = get_jwt_identity()
        total = PedidoService.total_vendido(usuario_id)
        mais_vendido = PedidoService.produto_mais_vendido(usuario_id)
        pedidos = PedidoService.listar_pedidos_hoje(usuario_id)
        return jsonify({
            "quantidade_pedidos": len(pedidos),
            "total_vendido": float(total),
            "produto_mais_vendido": mais_vendido,
            "pedidos": [pedido.to_dict() for pedido in pedidos] 
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500    

@pedido_bp.get('/funcionarios/pedidos/em_aberto')
@perfil_required('ADMINISTRADOR', 'GERENCIA', 'ATENDENTE', 'COZINHEIRO')
def pedidos_abertos():
    try:
        usuario_id = get_jwt_identity()
        pedidos = PedidoService.listar_pedidos_abertos(usuario_id)
        return jsonify([
            pedido.to_dict() for pedido in pedidos 
        ]), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500  


@pedido_bp.delete('/pedidos/<int:pedido_id>/itens/<int:item_id>')
@perfil_required('CLIENTE')
def remover_item_pedido(pedido_id, item_id):
    try:
        usuario_id = int(get_jwt_identity())
        pedido = PedidoService.remover_item(pedido_id,item_id,usuario_id)
        return jsonify ({
            "mensagem":"Item removido com sucesso",
            "pedido": pedido.to_dict()
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500     

