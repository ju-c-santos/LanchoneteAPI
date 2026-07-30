from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.status import Status
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.estoque_repository import EstoqueRepository


from datetime import datetime

class PedidoService:

    @staticmethod
    def criar_pedido(id, dados):
        if dados['observacao'] is '':
            dados['observacao'] = 'None'

        volume = len(dados['itempedido'])
        pedido = Pedido(
            usuario_id = id,
            unidade_id = dados['unidade_id'],
            observacao = dados['observacao'],
            data_pedido = datetime.now(),
            volume = volume
        )

        total = 0
        
        for item in dados['itempedido']:
            try:
                produto = EstoqueRepository.chase_by_id(item['produto_id'])
            except ValueError:
                return "Erro: Produto inexistente"
            if produto.is_active == False:
                raise ValueError('Erro: Produto indisponível') 
            
            valor_un = float(produto.preco)
            quantidade = int(item['quantidade'])
            subtotal = valor_un * quantidade

            total += subtotal

            novo_item = ItemPedido(
                estoque_id = produto.id,
                quantidade = item['quantidade'],
                preco = produto.preco,
                subtotal = subtotal, 
            )
            pedido.itempedido.append(novo_item)
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
    def finalizar(id_usuario, id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        if pedido.status != (Status.PRONTO, Status.AGUARDANDO_ENTREGADOR):
            raise ValueError("Status inválido")
        pedido.status = Status.FINALIZADO
        PedidoRepository.update()
        return pedido

    @staticmethod
    def cancelar(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido não encontrado")
        pedido.status = Status.CANCELADO
        PedidoRepository.update()
        return pedido
    