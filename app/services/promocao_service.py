from datetime import datetime
from decimal import Decimal
from app.models.promocao import Promocao
from app.models.descontos import TipoDesconto
from app.repositories.promocao_repository import PromocaoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.unidade_repository import UnidadeRepository
from app.util.api_response import resposta_sucesso
from app.util.api_error import ApiError
from app.util.conversores import Conversores
from decimal import Decimal, ROUND_HALF_UP

class PromocaoService:

    @staticmethod
    def create_promocao(dados):
        produto = ProdutoRepository.chase_by_id(dados['produto_id'])
        unidade = UnidadeRepository.chase_by_id(dados['unidade_id'])
        if produto is None:
            raise ApiError(
                error="PRODUTO_NAO_ENCONTRADO",
                message="O produto informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field": "produtoId",
                    "issue": f"O produto com Id {dados["produto_id"]} não existe."
                }]
            )
        elif unidade is None:
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidade informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field": "unidadeId",
                    "issue": f"A unidade com Id {dados["unidade_id"]} não existe."
                }]
            )
        try:
            tipo = TipoDesconto[dados['tipo_desconto'].upper()]
        except KeyError:
            raise ApiError(
                error="TIPO_DESCONTO_INVALIDO",
                message="O tipo de desconto informado é inválido",
                status_code=409,
                details=[{
                    "field": "tipoDesconto",
                    "issue": "Valores válidos: " + ", ".join(TipoDesconto)
                }]
            )
        valor = Decimal(str(dados['valor_desconto']))
        if valor <= 0:
            raise ApiError(
                error="DESCONTO_INVALIDO",
                message="O valor de desconto não pode ser abaixo de zero.",
                status_code=422,
                details=[{
                    "field": "valorDesconto",
                    "issue": "Insira um valor que seja maior ou igual a zero."
                }]
            )
        elif tipo == TipoDesconto.PERCENTUAL and 0 > valor > 100:
            raise ApiError(
                error="DESCONTO_INVALIDO",
                message="O percentual de desconto não pode ser menor que 0 e maior de 100.",
                status_code=422,
                details=[{
                    "field": "valorDesconto",
                    "issue": "Insira um valor que esteja entre 0 e 100."
                }]
            )
        data_inicio = datetime.fromisoformat(dados["data_inicio"])
        data_fim = datetime.fromisoformat(dados["data_fim"])
        if data_fim <= data_inicio:
            raise ApiError(
                error="DATA_FIM_INVALIDA",
                message="A data de fim deve ser maior que a data de início.",
                status_code=422,
                details=[{
                    "field": "dataFim",
                    "issue": "Insira uma data que seja posterior à data de início."
                }]
            )
        promocao = Promocao(
            nome = dados["nome"],
            produto_id = produto.id,
            unidade_id = unidade.id,
            tipo_desconto = tipo,
            valor_desconto = valor,
            quantidade_minima = int(dados['quantidade_minima']),
            data_inicio=data_inicio,
            data_fim=data_fim,
            ativa=True
        )
        return PromocaoRepository.save(promocao)

    @staticmethod
    def calcular_preco(produto, unidade_id, quantidade):
        quantidade = int(quantidade)
        preco = Decimal(str(produto.preco))
        promocao = (PromocaoRepository.chase_by_produto(produto.id_produto, unidade_id))
        if promocao is None:
            return preco
        if quantidade < promocao.quantidade_minima:
            return preco
        if promocao.ativa == False:
            return preco
        desconto = Decimal(str(promocao.valor_desconto))
        if promocao.tipo_desconto == TipoDesconto.PERCENTUAL:
            valor_desconto = preco * (desconto / Decimal("100"))
            preco_final = preco - valor_desconto
        elif promocao.tipo_desconto == TipoDesconto.VALOR_FIXO:
            preco_final = preco - desconto
        if preco_final < 0:
            preco_final = Decimal("0.00")
        preco_promocao = preco_final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return preco_promocao

    @staticmethod
    def atividade(promocao_id, bolv):
        promo = PromocaoRepository.chase_by_id(promocao_id)
        if promo is None:
            raise ApiError(
                error="PROMOCAO_NAO_ENCONTRADA",
                message="A promoção informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field": "promocaoId",
                    "issue": f"A promoção com Id {promocao_id} não existe."
                }]
            )
        nova_atualizacao = PromocaoRepository.update_activity(promocao_id, bolv)
        return nova_atualizacao

    @staticmethod
    def listar_promocao_filtrada(filtros):
        ordenacoes_permitidas={
            "promocaoId_asc",
            "promocaoId_desc",
            "nomePromo_asc",
            "nomePromo_desc",
            "dataPromo_asc",
            "dataPromo_desc"
        }
        page = filtros.get("pages", 1)
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
        if limit is None or limit < 1 or limit > 100:
            raise ApiError(
                error="LIMITE_INVALIDO",
                message="O limite deve ser entre 1 e 100.",
                status_code=422,
                details=[{
                    "field": "limit",
                    "issues": "São valores permitidos: 1 até 100."
                }]
            )
        promocao_id = Conversores.converter_id(filtros.get("promocao_id"), campo="promocaoId")
        produto_id = Conversores.converter_id(filtros.get("produto_id"), campo="produtoId")
        nome_promocao= filtros.get("nome_promocao")
        if nome_promocao:
            nome_promocao = nome_promocao.strip()
        tipo_promocao = Conversores.converter_enum(filtros.get("tipo_promocao"), enum_class=TipoDesconto, campo="tipoPromoco")
        ativa = Conversores.converter_booleano(filtros.get("ativa"), campo="ativa")
        data_inicio = Conversores.converter_data(filtros.get("data_inicio"), campo="dataInicio", fim_do_dia=False)
        data_fim = Conversores.converter_data(filtros.get("data_fim"), campo="dataFim", fim_do_dia=True)
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
        valor_min = Conversores.converter_decimal(filtros.get("valor_min"), campo="valorMin")
        valor_max = Conversores.converter_decimal(filtros.get("valor_max"), campo="valorMax")
        ordenacao = filtros.get("ordenar", "promocaoId_desc")
        if ordenacao not in ordenacoes_permitidas:
            raise ApiError(
                error="ORENACAO_INVALIDA",
                message="A ordenação informada é inválida.",
                status_code=422,
                details=[{
                    "field": "ordenar",
                    "issues": "Valores permitidos: " + ", ".join(ordenacoes_permitidas)
                }]
            )
        paginacao =(PromocaoRepository.listar_ativas(
            promocao_id= promocao_id,
            nome_promocao=nome_promocao,
            produto_id=produto_id,
            tipo_promocao=tipo_promocao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            valor_min=valor_min,
            valor_max=valor_max,
            ativa=ativa,
            ordenacao=ordenacao,
            page=page,
            limit=limit
        ))
        return {
            "promocoes":[
                promocao.to_dict()
                for promocao in paginacao.items
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
    def delete_promocao(promocao_id):
        promo = PromocaoRepository.chase_by_id(promocao_id)
        if promo is None:
            raise ApiError(
                error="PROMOCAO_NAO_ENCONTRADA",
                message="A promoção informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field": "promocaoId",
                    "issue": f"A promoção com Id {promocao_id} não existe."
                }]
            )
        return PromocaoRepository.delete(promo.id)