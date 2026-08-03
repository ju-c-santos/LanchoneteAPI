from datetime import datetime
from decimal import Decimal
from app.models.promocao import Promocao
from app.models.descontos import TipoDesconto
from app.repositories.promocao_repository import PromocaoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.unidade_repository import UnidadeRepository
from decimal import Decimal, ROUND_HALF_UP

class PromocaoService:

    @staticmethod
    def create_promocao(dados):
        produto = ProdutoRepository.chase_by_id(dados['produto_id'])
        unidade = UnidadeRepository.chase_by_id(dados['unidade_id'])
        if produto is None:
            raise ValueError("Produto não encontrado")
        elif unidade is None:
            raise ValueError("Unidade não encontrada")
        try:
            tipo = TipoDesconto[dados['tipo_desconto'].upper()]
        except KeyError:
            raise ValueError("Tipo de desconto inválido")
        valor = Decimal(str(dados['valor_desconto']))
        if valor <= 0:
            raise ValueError("Desconto não pode ser abaixo de 0")
        elif tipo == TipoDesconto.PERCENTUAL and valor > 100:
            raise ValueError("Percentual de desconto não pode ser acima de 100")
        data_inicio = datetime.fromisoformat(dados["data_inicio"])
        data_fim = datetime.fromisoformat(dados["data_fim"])
        if data_fim <= data_inicio:
            raise ValueError("erro: data_fim incorreta")
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