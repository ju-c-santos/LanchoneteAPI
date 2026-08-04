from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.status import Status
from app.models.pontos import Pontos
from app.models.local_pedido import LocalPedido
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.pagamento_repository import PagamentoRepository
from app.repositories.pontos_repository import PontosRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.relatorio_repository import RelatorioRepository
from app.services.promocao_service import PromocaoService
from app.services.pontos_service import PontosService
from app.repositories.itempedido_repository import ItemPedidoRepository

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

class PedidoService:

    @staticmethod
    def criar_pedido(id, dados):
        if dados['entrega'] == None:
            dados['entrega'] = False
        volume = len(dados['itempedido'])
        localpedido = dados['local_pedido'].upper().strip()
        usar_pontos = dados['usar_pontos']
        pedido = Pedido(
            usuario_id = id,
            unidade_id = dados['unidade_id'],
            observacao = dados['observacao'],
            data_pedido = datetime.now(),
            volume = volume, 
            entrega = dados['entrega'],
            local_pedido = LocalPedido[localpedido],
            usar_pontos = usar_pontos
        )
        total = Decimal("0.00")
        for item in dados['itempedido']:
            try:
                produto = EstoqueRepository.chase_by_id(item['produto_id'])
            except ValueError:
                return "Erro: Produto inexistente"
            if produto.is_active == False:
                raise ValueError('Erro: Produto indisponível')
            quantidade = int(item['quantidade'])
            valor_un = PromocaoService.calcular_preco(produto, pedido.unidade_id, quantidade)
            subtotal = (valor_un * quantidade).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total += subtotal
            pedido.total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            novo_item = ItemPedido(
                estoque_id = produto.id,
                quantidade = quantidade,
                preco = valor_un,
                subtotal = subtotal, 
            )
            pedido.itempedido.append(novo_item)
            EstoqueRepository.update_quantity_subtract(produto.id, quantidade)
        pedido = PedidoRepository.save(pedido)
        if usar_pontos:
            pontos_solicitado = dados['pontos_utilizados']
            if pontos_solicitado is None:
                raise ValueError("Quantidade de pontos inválida")
            PontosService.utilizar_pontos(int(id),pedido, pontos_solicitado)
            return pedido
        return pedido


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
        if pedido.status not in [Status.PRONTO, Status.AGUARDANDO_ENTREGADOR]:
            raise ValueError("Status inválido")
        pedido.status = Status.FINALIZADO
        PontosService.acumular_pontos(pedido)    
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
        for item in pedido.itempedido:
            EstoqueRepository.update_quantity_return(item.estoque_id, item.quantidade)
        PedidoRepository.update()
        return pedido


#SERVICES DE REQUISIÇÕES GET

    @staticmethod
    def historico_pedidos_all(usuario_id):
        pedidos = PedidoRepository.show_by_usuario(usuario_id)
        return [pedido.to_dict() for pedido in pedidos]


    @staticmethod
    def listar_pedidos_hoje(usuario_id):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        return PedidoRepository.show_today_all(funcionario.unidade_id)

    @staticmethod
    def total_vendido(usuario_id):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        return PedidoRepository.total_vendido_unidade(funcionario.unidade_id)

    @staticmethod
    def listar_pedidos_abertos(usuario_id):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        return PedidoRepository.show_today(funcionario.unidade_id)

    @staticmethod
    def produto_mais_vendido(usuario_id):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        resultado = RelatorioRepository.produto_mais_vendido_unidade(funcionario.unidade_id)
        return {
            "produto_id" : resultado.id,
            "nome" : resultado.nome,
            "total_vendido" : int(resultado.total_vendido)
        }

    @staticmethod
    def recalcular_total(pedido):
        total = Decimal("0.00")
        volume = 0
        for item in pedido.itempedido:
            total += Decimal(str(item.subtotal))
            volume += int(item.quantidade)
        pedido.total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        pedido.volume = volume


    @staticmethod
    def remover_item(pedido_id, item_id, usuario_id):
        pedido = PedidoRepository.chase_by_id(pedido_id)
        if pedido is None:
            raise ValueError("Pedido inválido")
        if pedido.usuario_id != usuario_id:
            raise ValueError("Você não possui autorização")
        if pedido.status != Status.AGUARDANDO_PAGAMENTO:
            raise ValueError("Pedido não pode ser alterado")
        item = ItemPedidoRepository.chase_by_id(item_id)
        if item is None or item.id_pedido != pedido.id:
            raise ValueError("Item não encontrado no pedido")
        estoque = EstoqueRepository.chase_by_id(item.estoque_id)
        if estoque is not None:
            estoque.quantidade += int(item.quantidade)
            estoque.is_active - True
        ItemPedidoRepository.delete(item)
        ItemPedidoRepository.flush()
        if len(pedido.itempedido) == 0:
            ItemPedidoRepository.delete(item)
            ItemPedidoRepository.update()
            return None
        PedidoService.recalcular_total(pedido)
        ItemPedidoRepository.update()
        return pedido

    @staticmethod
    def alterar_item(pedido_id, item_id, usuario_id, dados):
        pedido = PedidoRepository.chase_by_id(pedido_id)
        if pedido is None:
            raise ValueError("Pedido inválido")
        if pedido.usuario_id != usuario_id:
            raise ValueError("Você não possui autorização")
        if pedido.status != Status.AGUARDANDO_PAGAMENTO:
            raise ValueError("Pedido não pode ser alterado")
        item = ItemPedidoRepository.chase_by_id(item_id)
        if item is None or item.id_pedido != pedido.id:
            raise ValueError("Item não encontrado no pedido")         
        nova_quantidade = int(dados['quatidade'])
        if nova_quantidade <= 0:
            raise ValueError("A quantidade deve ser acima de zero")
        estoque = EstoqueRepository.chase_by_id(item.estoque_id)
        if estoque is None:
            raise ValueError("Estoque inválido")
        quantidade_anterior = int(item.quantidade)
        diferenca = nova_quantidade - quantidade_anterior
        #cliente aumentou a quantidade
        if diferenca > 0:
            if estoque.quantidade < diferenca:
                raise ValueError("Estoque insufuciente")
            estoque.quantidade -= diferenca

        #cliente diminuiu a quantidade
        elif diferenca < 0:
            estoque.quantidade += abs(diferenca)
            estoque.is_active = True
        valor_unitario = Decimal(str(item.preco))
        item.quantidade = nova_quantidade
        item.subtotal = (valor_unitario * Decimal(nova_quantidade)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        PedidoService.recalcular_total(pedido)
        PedidoRepository.update(pedido)
        return pedido
