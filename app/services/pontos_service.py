from app.models.pontos import Pontos
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.pontos_repository import PontosRepository
from decimal import Decimal, ROUND_HALF_UP

class PontosService:

    VALOR_POR_PONTO = Decimal("0.10")
    PONTOS_MINIMOS_USO = 50

    @staticmethod
    def atualizar_valor_desconto(usuario):
        usuario.valor_desconto = (
            Decimal(usuario.pontos_disponivel) * PontosService.VALOR_POR_PONTO
        ).quantize(Decimal("0.01"))


    @staticmethod
    def acumular_pontos(pedido):
        usuario = UsuarioRepository.chase_by_id(pedido.usuario_id)
        if usuario is None:
            raise ValueError("Usuario inexistente")
        movimentacao_existente = (PontosRepository.chase_by_pedido(pedido.id))
        if movimentacao_existente is not None:
            raise ValueError("Os pontos deste pedido já foram registrados")
        pontos_ganhos = int(pedido.volume)

        usuario.pontos_disponivel += pontos_ganhos
        PontosService.atualizar_valor_desconto(usuario)
        movimentacao = Pontos(
            usuario_id = usuario.id,
            pedido_id = pedido.id,
            tipo = 'GANHO',
            quantidade = pontos_ganhos
        )
        PontosRepository.save(movimentacao)
        PontosRepository.update()
        return movimentacao


    @staticmethod
    def consultar_saldo(usuario_id):
        usuario = UsuarioRepository.chase_by_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuário inexistente")

        desconto = (Decimal(usuario.pontos_disponivel) * Decimal("0.10")
        ).quantize(Decimal("0.01"))

        return {
            "pontos_disponiveis": usuario.pontos_disponivel,
            "valor_desconto": float(desconto),
            "pode_utilizar": usuario.pontos_disponivel >= 50
        } 


    @staticmethod
    def utilizar_pontos(usuario_id, pedido, pontos_solicitado):
        usuario = UsuarioRepository.chase_by_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuário inexistente")
        if usuario.pontos_disponivel < 50:
            raise ValueError("É necessário ter R$5,00 ou mais acumulados")
        if pontos_solicitado <= 0 :
            raise ValueError("Quantidade inválida")
        if pontos_solicitado > usuario.pontos_disponivel:
            raise ValueError("Saldo de pontos insuficiente")
        desconto = (Decimal(pontos_solicitado)*Decimal("0.10")).quantize(Decimal("0.01"))
        total_pedido = Decimal(str(pedido.total))
        usuario.pontos_disponivel -= pontos_solicitado
        pedido.total = total_pedido - desconto
        PontosService.atualizar_valor_desconto(usuario)
        movimentacao = Pontos(
            usuario_id = usuario.id,
            pedido_id = pedido.id,
            tipo = 'RESGATE',
            quantidade = pontos_solicitado
        )
        PontosRepository.save(movimentacao)
        PontosRepository.update()
        return {
            "pontos_utilizados": pontos_solicitado,
            "desconto": desconto,
            "total_final": pedido.total,
            "saldo_pontos": usuario.pontos_disponivel
        }

                        
            

