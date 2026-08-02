from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.status import Status
from app.models.pontos import Pontos
from app.models.local_pedido import LocalPedido
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.pagamento_repository import PagamentoRepository
from app.repositories.pontos_repository import PontosRepository

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

class PedidoService:

    @staticmethod
    def criar_pedido(id, dados):
        if dados['observacao'] is '':
            dados['observacao'] = 'None'
        if dados['entrega'] == None:
            dados['entrega'] = False
        volume = len(dados['itempedido'])
        localpedido = dados['local_pedido'].upper()
        pedido = Pedido(
            usuario_id = id,
            unidade_id = dados['unidade_id'],
            observacao = dados['observacao'],
            data_pedido = datetime.now(),
            volume = volume, 
            entrega = dados['entrega'],
            local_pedido = LocalPedido[localpedido]
        )

        total = Decimal("0.00")


        for item in dados['itempedido']:
            try:
                produto = EstoqueRepository.chase_by_id(item['produto_id'])
            except ValueError:
                return "Erro: Produto inexistente"
            if produto.is_active == False:
                raise ValueError('Erro: Produto indisponível') 
            valor_un = Decimal(str(produto.preco))
            quantidade = Decimal(str(item['quantidade']))
            subtotal = (valor_un * quantidade).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total += subtotal
            pedido.total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            novo_item = ItemPedido(
                estoque_id = produto.id,
                quantidade = item['quantidade'],
                preco = produto.preco,
                subtotal = subtotal, 
            )
            pedido.itempedido.append(novo_item)
            EstoqueRepository.update_quantity(produto.id, quantidade)
        pedido.total = total
        return PedidoRepository.save(pedido)


    @staticmethod
    def preparar_pedido(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        if pedido.status != Status.AGUARDANDO_CONFIRMACAO:
            raise ValueError("Status inválido")
        pedido.status = Status.EM_PREPARO
        PedidoRepository.update()
        return pedido

    @staticmethod
    def pedido_pronto(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        if pedido.status != Status.EM_PREPARO:
            raise ValueError("Status inválido")
        pedido.status = Status.PRONTO
        PedidoRepository.update()
        return pedido

    @staticmethod
    def aguardando_entregador(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido.entrega == False:
            raise ValueError("Status inválido")
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        if pedido.status != Status.PRONTO:
            raise ValueError("Status inválido")
        pedido.status = Status.AGUARDANDO_ENTREGADOR
        PedidoRepository.update()
        return pedido

    @staticmethod
    def finalizar(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        if pedido.entrega and pedido.status != Status.AGUARDANDO_ENTREGADOR:
            raise ValueError("Pedido não foi entregue")
        if pedido.status not in [Status.PRONTO or Status.AGUARDANDO_ENTREGADOR]:
            raise ValueError("Status inválido")
        pedido.status = Status.FINALIZADO
        usuario = PontosRepository.chase_by_id(pedido.usuario_id)
        if usuario:
            usuario.pontos += pedido.volume
            PontosRepository.update()
        else:
            novo = Pontos(
                usuario_id = pedido.usuario_id,
                pedido_id = id_pedido,
                pontos = pedido.volume
            )
            PontosRepository.save(novo)
        PedidoRepository.update()
        return pedido

    @staticmethod
    def cancelar(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        pagamento = PagamentoRepository.chase_by_pedido(pedido.id)
        if pagamento.aprovado == False:
            pedido.status = Status.CANCELADO
        pedido.status = Status.CANCELADO
        PedidoRepository.update()
        return pedido
    