from app.models.pontos import Pontos
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.pontos_repository import PontosRepository
from decimal import Decimal, ROUND_HALF_UP
from app.util.api_error import ApiError

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
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {pedido.usuario_id} não existe."
                }]
            )
        movimentacao_existente = (PontosRepository.chase_by_pedido(pedido.id))
        if movimentacao_existente is not None:
            raise ApiError(
                error="PONTOS_JA_REGISTRADOS",
                message="Os pontos deste pedido já foram registrados.",
                status_code=422,
                details=[]
            )
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
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {usuario_id} não existe."
                }]
            )
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
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {usuario_id} não existe."
                }]
            )
        if usuario.pontos_disponivel <= 50:
            raise ApiError(
                error="SALDO_INSUFICIENTE",
                message="O saldo de pontos para uso é insuficiente.",
                status_code=409,
                details=[{
                    "field":"pontosDisponivel",
                    "issue":f"São necessários 50 pontos ou mais acumulados para utilizar, você possui {usuario.pontos_disponivel} ."
                }]
            )
        if pontos_solicitado <= 0 :
            raise ApiError(
                error="QUANTIDADE_INVALIDA",
                message="A quantidade informada é inválida.",
                status_code=422,
                details=[{
                    "field":"pontosSolicitados",
                    "issue":"São aceitos apenas valores acima de 0."
                }]
            )
        if pontos_solicitado > usuario.pontos_disponivel:
            raise ApiError(
                error="SALDO_INSUFICIENTE",
                message="O saldo de pontos do usuário é inuficiente.",
                status_code=409,
                details=[]
            )
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

                        
            

