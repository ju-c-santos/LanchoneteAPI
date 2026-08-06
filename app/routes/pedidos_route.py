from flask import Blueprint, request, jsonify
from app.services.pedido_service import PedidoService
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity
from app.models.local_pedido import LocalPedido
from app.util.api_error import ApiError
from app.util.api_response import resposta_sucesso

pedido_bp = Blueprint("pedido", __name__)

@pedido_bp.route("/login/pedidos", methods=['POST'])
@perfil_required("CLIENTE")
def criar_pedido():
    usuario_id = get_jwt_identity()
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        )
    canal_recebido = dados['canalPedido']
    if canal_recebido is None:
        raise ApiError(
            error="CAMPO_OBRIGATORIO",
            message="O campo canalPedido é obrigatório.",
            status_code=422,
            details=[{
                "field":"canalPedido",
                "issue":"Campo não informado."
            }]
        ) 
    if not isinstance(canal_recebido, str):
        raise ApiError(
            error="TIPO_INVALIDO",
            message="O campo canalPedido deve ser uma string.",
            status_code=422,
            details=[{
                "field":"canalPedido",
                "issue":"Informe um valor textual."
            }]
        )
    canal_recebido = canal_recebido.upper().strip()
    if canal_recebido not in LocalPedido:
        valores_permitidos = [
            canal.value for canal in LocalPedido
        ]
        raise ApiError(
            error="CANAL_PEDIDO_INVALIDO",
            message="O canal do pedido informado não é válido.",
            status_code=422,
            details=[{
                "field":"canalPedido",
                "issue":"Valores permitidos:" + ", ".join(valores_permitidos)
                }]
        )
    pedido = PedidoService.criar_pedido(usuario_id, dados)
    return resposta_sucesso(
        message="Pedido criado com sucesso!",
        status_code=201,
        data=pedido.to_dict()
    )

#ROTAS PARA ALTERAÇÃO DE STATUS
@pedido_bp.patch("/<int:id>/status/aceitar")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def aceitar_pedido(id):
    pedido = PedidoService.preparar_pedido(id)
    return resposta_sucesso(
        message="Pedido aceito e enviado para preparo.",
        status_code=200,
        data={
            "pedidoId": pedido.id,
            "status": pedido.status.value,
            "unidadeId": pedido.unidade_id,
            "usuarioId": pedido.usuario_id,
            "dataPedido": pedido.data_pedido.isoformat()
        }
    )

@pedido_bp.patch("/<int:id>/status/pronto")
@perfil_required("COZINHEIRO", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def pedido_pronto(id):
    pedido = PedidoService.pedido_pronto(id)
    return resposta_sucesso(
        message="Pedido pronto.",
        status_code=200,
        data={
            "pedidoId": pedido.id,
            "status": pedido.status.value,
            "unidadeId": pedido.unidade_id,
            "usuarioId": pedido.usuario_id,
            "dataPedido": pedido.data_pedido.isoformat()
        }
    )

@pedido_bp.patch("/<int:id>/status/entrega")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def pedido_entrega(id):
    pedido = PedidoService.aguardando_entregador(id)
    return resposta_sucesso(
        message="Pedido saiu para entrega.",
        status_code=200,
        data={
            "pedidoId": pedido.id,
            "status": pedido.status.value,
            "unidadeId": pedido.unidade_id,
            "usuarioId": pedido.usuario_id,
            "dataPedido": pedido.data_pedido.isoformat()
        }
    )

@pedido_bp.patch("/<int:id>/status/finalizar")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def finalizar(id):
    pedido = PedidoService.finalizar(id)
    return resposta_sucesso(
        message="Pedido finalizado.",
        status_code=200,
        data={
            "pedidoId": pedido.id,
            "status": pedido.status.value,
            "unidadeId": pedido.unidade_id,
            "usuarioId": pedido.usuario_id,
            "dataPedido": pedido.data_pedido.isoformat()
        }
    )

@pedido_bp.patch("/<int:id>/status/cancelar")
@perfil_required("ATENDENTE", "GERENCIA", "ADMINISTRADOR", "GESTAO")
def cancelar(id):
    pedido = PedidoService.cancelar(id)
    return resposta_sucesso(
        message="Pedido cancelado.",
        status_code=200,
        data={
            "pedidoId": pedido.id,
            "status": pedido.status.value,
            "unidadeId": pedido.unidade_id,
            "usuarioId": pedido.usuario_id,
            "dataPedido": pedido.data_pedido.isoformat()
        }
    )

@pedido_bp.patch("/pedidos/<int:pedido_id>/itens/<int:itempedido_id>/alterar")
@perfil_required("CLIENTE")
def alterar_item_pedido(pedido_id, itempedido_id):
    usuario_id = int(get_jwt_identity())
    dados = request.get_json()
    pedido = PedidoService.alterar_item(pedido_id, itempedido_id, usuario_id, dados)
    return resposta_sucesso(
        message="Item do pedido foi alterado com sucesso!",
        status_code=200,
        data=pedido.to_dict()
    )
 
#ROTAS PARA RETORNO
#para o usuario mostra apenas os pedidos do usuario
@pedido_bp.get('/login/pedidos/historico')
@perfil_required('CLIENTE')
def historico_cliente():
    filtros = {
        "data_inicio": request.args.get("dataInicio"),#DATATIME
        "data_fim": request.args.get("dataFim"),#DATATIME
        "unidade_id": request.args.get("unidadeId"),
        "status": request.args.get("status"),#ENUM
        "pedido_id": request.args.get("pedidoId"),
        "canal_pedido": request.args.get("canalPedido"),#ENUM
        "entrega": request.args.get("entrega"),#BOOL
        "valor_min": request.args.get("valorMin"), #DECIMAL
        "valor_max": request.args.get("valorMax"), #DECIMAL
        "ordenar": request.args.get("ordenar", default="pedidoId_desc"),####
        "page": request.args.get("page", default=1, type=int),
        "limit": request.args.get("limit", default=20, type=int)
    }
    usuario_id = int(get_jwt_identity())
    pedidos = PedidoService.historico_pedidos_all(usuario_id, filtros)
    return resposta_sucesso( 
        message = "Histórico de pedidos consultado com sucesso.",
        data = pedidos["pedidos"],
        meta=pedidos["meta"],
        status_code=200
    )

#rota para administradores mostra TUUDOOO
@pedido_bp.get('/admin/pedidos/historico/<int:usuario_id>')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO") 
def historico_cliente_adm(usuario_id):
    filtros = {
        "data_inicio": request.args.get("dataInicio"),#DATATIME
        "data_fim": request.args.get("dataFim"),#DATATIME
        "unidade_id": request.args.get("unidadeId"),
        "status": request.args.get("status"),#ENUM
        "pedido_id": request.args.get("pedidoId"),
        "canal_pedido": request.args.get("canalPedido"),#ENUM
        "entrega": request.args.get("entrega"),#BOOL
        "valor_min": request.args.get("valorMin"), #DECIMAL
        "valor_max": request.args.get("valorMax"), #DECIMAL
        "ordenar": request.args.get("ordenar", default="pedidoId_desc"),####
        "page": request.args.get("page", default=1, type=int),
        "limit": request.args.get("limit", default=20, type=int)
    }
    pedidos = PedidoService.historico_pedidos_all(usuario_id, filtros)
    return resposta_sucesso( 
        message = "Histórico de pedidos consultado com sucesso.",
        data = pedidos["pedidos"],
        meta=pedidos["meta"],
        status_code=200
    )
     

#MOSTRA TODOS OS PEDIDOS DO DIIIIAAAAA
@pedido_bp.get('/admin/pedidos')
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
def pedidos_hoje():
    filtros = {
        "unidade_id": request.args.get("unidadeId"),##
        "status": request.args.get("status"),##
        "pedido_id": request.args.get("pedidoId"),##
        "entrega": request.args.get("entrega"),##
        "canal_pedido": request.args.get("canalPedido"),##
        "valor_min": request.args.get("valorMin"),#
        "valor_max": request.args.get("valorMax"),#
        "hora_inicio": request.args.get("horaInicio"),
        "hora_fim": request.args.get("horaFim"),
        "ordenar": request.args.get("page", default="pedidoId_desc"),###
        "page": request.args.get("page", default=1, type=int),###
        "limit": request.args.get("limit", default=20, type=int)###
    }
    usuario_id = get_jwt_identity()
    total = PedidoService.total_vendido(usuario_id)
    mais_vendido = PedidoService.produto_mais_vendido(usuario_id)
    pedidos = PedidoService.listar_pedidos_hoje(usuario_id, filtros)
    return resposta_sucesso(
        message="Histórico de pedidos do dia consultado com sucesso.",
        data={
            "total_vendido":total,
            "produto_mais_vendido": mais_vendido,
            "pedidos": pedidos["pedidos"]   
        },
        meta=pedidos["meta"],
        status_code=200
    )
    

#APENAS OS PEDIDOS EM ABEEERRTOOOO
@pedido_bp.get('/funcionarios/pedidos/em_aberto')
@perfil_required('ADMINISTRADOR', 'GERENCIA', 'ATENDENTE', 'COZINHEIRO', "GESTAO")
def pedidos_abertos():####INSERIR FILTROS########

    usuario_id = get_jwt_identity()
    pedidos = PedidoService.listar_pedidos_abertos(usuario_id)
    return jsonify([
    pedido.to_dict() for pedido in pedidos 
        ]), 200
   

@pedido_bp.delete('/pedidos/<int:pedido_id>/itens/<int:itempedido_id>/delete')
@perfil_required("CLIENTE")
def remover_item_pedido(pedido_id, itempedido_id):
    usuario_id = int(get_jwt_identity())
    pedido = PedidoService.remover_item(pedido_id,itempedido_id,usuario_id)
    return resposta_sucesso(
        message="Item do pedido foi deletado com sucesso!",
        status_code=200,
        data=pedido.to_dict()
    )
 
  

