from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.status import Status
from app.models.pontos import Pontos
from app.models.local_pedido import LocalPedido
from app.services.estoque_service import EstoqueService
from app.repositories.unidade_repository import UnidadeRepository
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.pagamento_repository import PagamentoRepository
from app.repositories.pontos_repository import PontosRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.relatorio_repository import RelatorioRepository
from app.services.promocao_service import PromocaoService
from app.services.pontos_service import PontosService
from app.repositories.itempedido_repository import ItemPedidoRepository
from datetime import datetime, time
from decimal import Decimal, InvalidOperation
from app.util.api_error import ApiError
from app.util.conversores import Conversores

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

class PedidoService:

    @staticmethod
    def criar_pedido(id, dados):
        if dados['entrega'] == None:
            dados['entrega'] = False
        volume = len(dados['itempedido'])
        usar_pontos = dados['usarPontos']
        pedido = Pedido(
            usuario_id = id,
            unidade_id = dados['unidadeId'],
            observacao = dados['observacao'],
            data_pedido = datetime.now(),
            volume = volume, 
            entrega = dados['entrega'],
            local_pedido = dados['canalPedido'],
            usar_pontos = usar_pontos
        )
        total = Decimal("0.00")
        for item in dados['itempedido']:
            try:
                produto = EstoqueRepository.chase_by_id(item['produtoId'])
            except ValueError:
                return ApiError(
                error="PRODUTO_NAO_ENCONTRADO",
                message="O produto não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"produtoId",
                    "issue": f"O produto {produto.id} não foi encontrado."
                }]
            )
            if produto.is_active == False:
                raise ApiError(
                error="PRODUTO_INDISPONIVEL",
                message="O protuto se encontra indisponível em estoque no momento.",
                status_code=409,
                details=[]
            )
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
                raise ApiError(
                error="QUANTIDADE_PONTOS_INVALIDA",
                message="A quantidade de pontos é inválida.",
                status_code=409,
                details=[{
                    "field":"pontos_solicitado",
                    "issue": f"Só é possível utilizar pontos com um total acumulado acima de 50."
                }]
            )
            PontosService.utilizar_pontos(int(id),pedido, pontos_solicitado)
            return pedido
        return pedido

    @staticmethod
    def preparar_pedido(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {id_pedido} não foi encontrado."
                }]
            )
        if pedido.status != Status.AGUARDANDO_CONFIRMACAO:
            raise ApiError(
                error="STATUS_INVALIDO",
                message="Campo status se ecnontra inválido.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue": f"Somente pedidos com status {Status.AGUARDANDO_CONFIRMACAO}, podem iniciar preparo."
                }]
            )
        pedido.status = Status.EM_PREPARO
        PedidoRepository.update()
        return pedido

    @staticmethod
    def pedido_pronto(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {id_pedido} não foi encontrado."
                }]
            )
        if pedido.status != Status.EM_PREPARO:
            raise ApiError(
                error="STATUS_INVALIDO",
                message="Campo status se ecnontra inválido.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue": f"Somente pedidos com status {Status.EM_PREPARO}, podem ser prontos."
                }]
            )
        pedido.status = Status.PRONTO
        PedidoRepository.update()
        return pedido

    @staticmethod
    def aguardando_entregador(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido.entrega == False:
            raise ApiError(
                error="STATUS_INVALIDO",
                message="Campo status se ecnontra inválido.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue":"Pedido marcado como retirada devem ser buscados pelo cliente."
                }]
            )
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {id_pedido} não foi encontrado."
                }]
            )
        if pedido.status != Status.PRONTO:
            raise ApiError(
                error="STATUS_INVALIDO",
                message="Campo status se encontra inválido.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue": f"Somente pedidos com status {Status.PRONTO}, podem ser entregue ao entregador. "
                }]
            )
        pedido.status = Status.AGUARDANDO_ENTREGADOR
        PedidoRepository.update()
        return pedido

    @staticmethod
    def finalizar(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {id_pedido} não foi encontrado."
                }]
            )
        if pedido.entrega and pedido.status != Status.AGUARDANDO_ENTREGADOR:
            raise ApiError(
                error="PEDIDO_NAO_ENTREGUE",
                message="O pedido não foi entregue.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue":"O pedido só pode ser finalizado depois de entregue."
                }]
            )
        if pedido.status not in [Status.PRONTO, Status.AGUARDANDO_ENTREGADOR]:
            raise ApiError(
                error="STATUS_INVALIDO",
                message="Campo status se ecnontra inválido.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue": f"Somente pedidos com status {Status.PRONTO} ou {Status.AGUARDANDO_ENTREGADOR}, podem ser finalizados. "
                }]
            )
        pedido.status = Status.FINALIZADO
        PontosService.acumular_pontos(pedido)    
        return pedido

    @staticmethod
    def cancelar(id_pedido):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {id_pedido} não foi encontrado."
                }]
            )
        pagamento = PagamentoRepository.chase_by_pedido(pedido.id)
        if pagamento.aprovado == False:
            pedido.status = Status.CANCELADO
        pedido.status = Status.CANCELADO
        for item in pedido.itempedido:
            if item.estoque_id is None:
                raise ApiError(
                error="ITEM_NAO_ENCONTRADO",
                message="O item não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"itemEstoqueId",
                    "issue": f"o item {item.estoque_id} não foi encontrado no pedido."
                }]
            )
            EstoqueRepository.update_quantity_return(item.estoque_id, item.quantidade)
        PedidoRepository.update()
        return pedido

#SERVICES DE REQUISIÇÕES GET

    @staticmethod
    def historico_pedidos_all(usuario_id, filtros):
        ordenacoes_permitidas = {
            "pedidoId_asc",
            "pedidoId_desc",
            "dataPedido_asc",
            "dataPedido_desc",
            "valorTotal_asc",
            "valotTotal_desc"
        }
        page = filtros.get("page", 1)
        limit = filtros.get("limit", 20)
        if page is None or page < 1:
            raise ApiError(
                error="PAGINA_INVALIDA",
                message="A página deve ser maior que um.",
                status_code=422,
                details=[{
                    "field": "page",
                    "issue": "Informe um número que seja maior que um."
                }]
            )
        if limit is None or limit < 1 or limit > 100:
            raise ApiError(
                error="LIMTE_INVALIDO",
                message="O limite deve ser entre 1 e 100.",
                status_code=422,
                details=[{
                    "field":"limit",
                    "issue":"São Valores permitidos: 1 até 100."
                }]
            )
        unidade_id = Conversores.converter_id(filtros.get("unidade_id"), campo="unidadeId")
        if unidade_id is not None:
            unidade = UnidadeRepository.chase_by_id(unidade_id)
        
        if unidade is None:
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidde informada não foi encontrada.",
                status_code=404,
                details=[{
                    "fields":"unidadeId",
                    "issue": f"Não existe unidade com o Id {unidade_id}."
                }]
            )

        pedido_id = Conversores.converter_id(filtros.get("pedido_id", campo="pedidoId"))
        if pedido_id is not None:
            pedido = PedidoRepository.chase_by_id_user(pedido_id, usuario_id)
            if pedido is None:
                raise ApiError(
                    error="PEDIDO_NAO_ENCONTRADO",
                    message="O pedido informado não foi encontrado.",
                    status_code=404,
                    details=[{
                        "field":"pedidoId",
                        "issue":f"O pedido {pedido_id} não existe ou não pertence ao usuário logado."
                    }]
                )
    
            if unidade_id is not None and pedido.unidade_id != unidade_id:
                #verifica se o pedido a unidade_id informada é a mesma que tá no pedido
                raise ApiError(
                    error="PEDIDO_NAO_PERTENCE_UNIDADE",
                    message="O pedido não pertence à unidade informada.",
                    status_code=409,
                    details=[{
                        "field":"unidadeId",
                        "issue":f"O pedido {pedido_id} pertence à unidade {pedido.unidade_id}"
                    }]
                )
        data_inicio = Conversores.converter_data(filtros.get(data_inicio), "dataInicio", False) #este inicia de manhâ
        data_fim = Conversores.converter_data(filtros.get(data_fim), "dataFim", True)# este vai até o fim do dia
        if data_inicio is not None and data_fim is not None and data_inicio > data_fim:
            raise ApiError(
                error="PERIODO_INVALIDO",
                message="A data inicial não pode ser depois da final.",
                status_code=422,
                details=[{
                    "field":"dataInicio",
                    "issue":"A data inicial deve ser aterior à data final."
                }]
            )
        status = Conversores.converter_enum(filtros.get("canal_pedido"), Status, "status")
        canal_pedido = Conversores.converter_enum(filtros.get("canal_pedido", LocalPedido, "canalPedido"))
        entrega = Conversores.converter_booleano(filtros.get("entrega", "entrega"))
        valor_min = Conversores.converter_decimal(filtros.get("valor_min", "ValorMin"))
        valor_max = Conversores.converter_decimal(filtros.get("valor_max", "ValorMax"))
        if valor_min is not None and valor_max is not None and valor_min > valor_max:
            raise ApiError(
                error="INTERVALO_INVALIDO",
                message="O valor mínimo deve ser menor ou igual que o máximo.",
                status_code=422,
                details=[{
                    "field":"valorMin",
                    "issue":"Deve ser menor ou igual ao valor máximo."
                }]
            )
        ordenar = filtros.get("ordenar", "pedidoId_desc")
        if ordenar not in ordenacoes_permitidas:
            raise ApiError(
                error="ORDENACAO_INVALIDA",
                message="A ordenação informada é inválida.",
                status_code=422,
                details=[{
                    "field":"ordenar",
                    "issue":"Valores permitidos: " + ", ".join(sorted(ordenacoes_permitidas))
                }]
            )
        paginacao = (
            PedidoRepository.show_by_usuario(
                usuario_id, pedido_id, unidade_id, status,
                canal_pedido, entrega, data_inicio, data_fim, 
                valor_min, valor_max, ordenar, page, limit
            )
        )
        return {
            "pedidos": [
                pedido.to_dict()
                for pedido in paginacao.items
            ],
            "meta":{
                "page": paginacao.page,
                "limit": limit,
                "totalItems": paginacao.total,
                "totalPages": paginacao.pages,
                "hasNext": paginacao.has_next,
                "hasPrevious": paginacao.has_prev
            }
        }

    @staticmethod
    def listar_pedidos_hoje(usuario_id, filtros):
        ordenacoes_permitidas ={
            "pedidoId_asc",
            "pedidoId_desc",
            "valor_asc",
            "valor_desc"
        }
        page = filtros.get("page", 1)
        limit = filtros.get("limit", 20)
        if page is None or page < 1:
            raise ApiError(
                error="PAGINA_INVALIDA",
                message="A página deve ser maior que um.",
                status_code=422,
                details=[{
                    "field": "page",
                    "issues": "Informe um número que seja maior que um."
                }]
            )
        if limit is None or 1 > limit > 100:
            raise ApiError(
                error="LIMITE_INVALIDO",
                message="O limite deve ser entre 1 e 100.",
                status_code=422,
                details=[{
                    "field": "limit",
                    "issues": "São valores permitidos: 1 até 100."
                }]
            )
        unidade_id = Conversores.converter_id(filtros.get("unidade_id"), "unidadeId")
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        if unidade_id is None:
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidade informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field": "unidadeId",
                    "issues": f"Não existe unidade com Id {unidade_id}."
                }]
            )
        if funcionario.id is not None and funcionario.unidade_id != unidade_id:
            raise ApiError(
                error="FUNCIONARIO_SEM_PERMISSAO",
                message="Funcionário sem permissão para visualizar histórico.",
                status_code=409,
                details=[{
                    "field": "usuarioId",
                    "issues": "Um funcionário só pode ter acesso ao histórico de pedidos de sua própia unidade."
                }]
            )
        pedido_id = Conversores.converter_id(filtros.get("pedido_id"))
        if pedido_id is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field": "pedidoId",
                    "issues": f"O pedido {pedido_id} não existe."
                }]
            )
        pedido = PedidoRepository.chase_by_id(pedido_id)
        if unidade_id is not None and pedido.unidade_id != unidade_id:
            raise ApiError(
                error="PEDIDO_NAO_PERTENCE_UNIDADE",
                message="O pedido informado não pertence à unidade.",
                status_code=422,
                details=[{
                    "field": "pedidoId",
                    "issues": f"O pedido{pedido_id} pertence à unidade {pedido.unidade_id}."
                }]
            )
        status = Conversores.converter_enum(filtros.get("status"), Status, "status")
        canal_pedido = Conversores.converter_enum(filtros.get("canal_pedido"), LocalPedido, "canalPedido")
        entrega = Conversores.converter_booleano(filtros.get("entrega"), "entrega")
        valor_min = Conversores.converter_decimal(filtros.get("valor_min"), "valorMin")
        valor_max = Conversores.converter_decimal(filtros.get("valor_max"), "valorMax")
        if valor_min is not None and valor_max is not None and valor_min > valor_max:
            raise ApiError(
                error="INTERVALO_INVALIDO",
                message="O valor mínimo deve ser menor ou igual ao máximo.",
                status_code=422,
                details=[{
                    "field": "valorMin",
                    "issues": "Deve ser menor ou igual ao valor máximo."
                }]
            )
        hora_inicio = Conversores.converter_hora(filtros.get("hora_inicio"), "horaInicio")
        hora_fim = Conversores.converter_hora(filtros.get("hora_fim"), "horaFim")
        if hora_fim is not None and hora_inicio is not None and hora_fim > hora_inicio:
            raise ApiError(
                error="PERIODO_INVALIDO",
                message="O horário final não pode ser mais tarde que o horário inicial.",
                status_code=422,
                details=[{
                    "field": "horaInicio",
                    "issues": "Deve ser menor que o horário final."
                }]
            )
        ordenar = filtros.get("ordenar", "pedidoId_desc")
        if ordenar not in ordenacoes_permitidas:
            raise ApiError(
                error="ORENACAO_INVALIDA",
                message="A ordenação informada é inválida.",
                status_code=422,
                details=[{
                    "field": "ordenar",
                    "issues": "Valores permitidos: " + ", ".join(ordenacoes_permitidas)
                }]
            )
        unidade_id = funcionario.unidade_id
        paginacao = (PedidoRepository.show_today_all(
            usuario_id, pedido_id, unidade_id, status, canal_pedido,
            entrega, hora_inicio, hora_fim, valor_min, valor_max, ordenar, page, limit  
            ))
        return{
            "pedidos":[
                pedido.to_dict()
                for pedido in paginacao.items
            ],
            "meta":{
                "page": paginacao.page,
                "limit": limit,
                "totalItems": paginacao.total,
                "totalPages": paginacao.pages,
                "hasNext": paginacao.has_next,
                "hasPrevious": paginacao.has_prev
            }
        }
        

    @staticmethod
    def total_vendido(usuario_id):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        return PedidoRepository.total_vendido_unidade(funcionario.unidade_id)

    @staticmethod
    def listar_pedidos_abertos(usuario_id, filtros):#########
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
        for item in pedido.itempedido:
            total += Decimal(str(item.subtotal))
        pedido.total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def remover_item(pedido_id, item_id, usuario_id):
        pedido = PedidoRepository.chase_by_id(pedido_id)
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {pedido_id} não foi encontrado."
                }]
            )
        if pedido.usuario_id != usuario_id:
            raise ApiError(
                error="USUARIO_NAO_AUTORIZADo",
                message="Usuário não autorizado para realizar edições.",
                status_code=403,
                details=[{
                    "field":"usuarioId",
                    "issue": "Apenas o usuário que realizou o pedido pode fazer alterações."
                }]
            )
        if pedido.status != Status.AGUARDANDO_PAGAMENTO:
            raise ApiError(
                error="ALTERACAO_NAO_AUTORIZADA",
                message="O pedido não pode mais ser alterado.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue": f"Status atual: {pedido.status}."
                }]
            )
        pedido.volume -= 1
        item = ItemPedidoRepository.chase_by_id(item_id)
        if item is None or item.id_pedido != pedido.id:
            raise ApiError(
                error="ITEM_NAO_ENCONTRADO",
                message="O item não foi encontrado no pedido.",
                status_code=404,
                details=[{
                    "field":"itemId",
                    "issue": f"O item {item.id} não foi encontrado no pedido {pedido.id}."
                }]
            )
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
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue": f"O pedido {pedido_id} não foi encontrado."
                }]
            )
        if pedido.usuario_id != usuario_id:
            raise ApiError(
                error="USUARIO_NAO_AUTORIZADo",
                message="Usuário não autorizado para realizar edições.",
                status_code=403,
                details=[{
                    "field":"usuarioId",
                    "issue": "Apenas o usuário que realizou o pedido pode fazer alterações."
                }]
            )
        if pedido.status != Status.AGUARDANDO_PAGAMENTO:
            raise ApiError(
                error="ALTERACAO_NAO_AUTORIZADA",
                message="O pedido não pode mais ser alterado.",
                status_code=409,
                details=[{
                    "field":"status",
                    "issue": f"Status atual: {pedido.status}."
                }]
            )
        item = ItemPedidoRepository.chase_by_id(item_id)
        if item is None or item.id_pedido != pedido.id:
            raise ApiError(
                error="ITEM_NAO_ENCONTRADO",
                message="O item informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"itemId",
                    "issue": f"O item {item} não foi encontrado no pedido."
                }]
            )    
        nova_quantidade = int(dados['quantidade'])
        if nova_quantidade <= 0:
            raise ApiError(
                error="NOVA_QUANTIDADE_INVALIDA",
                message="A nova quantidade informada é menor ou igual a zero.",
                status_code=422,
                details=[{
                    "field":"quantidade",
                    "issue": f"A quantidade deve ser um número acima de zero."
                }]
            )
        estoque = EstoqueRepository.chase_by_id(item.estoque_id)
        if estoque is None:
            raise ApiError(
                error="ITEM_NAO_ENCONTRADO",
                message= "O item informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"itemEstoqueId",
                    "issue": f"O item {item.estoque_id} não foi encontrado no estoque."
                }]
            )
        quantidade_anterior = int(item.quantidade)
        diferenca = nova_quantidade - quantidade_anterior
        #cliente aumentou a quantidade
        if diferenca > 0:
            if estoque.quantidade < diferenca:
                raise ApiError(
                error="ESTOQUE_INSUFICIENTE",
                message="O item desejado não se encontra mais em estoque.",
                status_code=409,
                details=[]
            )
            estoque.quantidade -= diferenca
        #cliente diminuiu a quantidade
        elif diferenca < 0:
            estoque.quantidade += abs(diferenca)
            estoque.is_active = True
        valor_unitario = Decimal(str(item.preco))
        item.quantidade = nova_quantidade
        item.subtotal = (valor_unitario * Decimal(nova_quantidade)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        PedidoService.recalcular_total(pedido)
        PedidoRepository.update()
        return pedido
