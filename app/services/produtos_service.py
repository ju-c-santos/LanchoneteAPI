from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.models.historico_preco import HistoricoPreco
from app.repositories.historico_preco_repository import HistoricoPrecoRepository
from decimal import Decimal

class ProdutoService:

    @staticmethod
    def novoProduto(dados):
        produto_exists = ProdutoRepository.chase_by_name(dados['nome'])
        if produto_exists:
            raise ValueError("Produto já existente")
        produto = Produto(
            nome = dados['nome'],
            preco = dados['preco'],
            categoria = dados['categoria'],
            descricao = dados['descricao']
        )
        return ProdutoRepository.save(produto)

    @staticmethod
    def alterarValor(produto_id, usuario_id, dados):
        produto = ProdutoRepository.chase_by_id(produto_id)
        if produto is None: 
            raise ValueError("Produto não encontrado")
        novo_valor = Decimal(str(dados['novo_valor']))
        if novo_valor <= 0:
            raise ValueError("O preço deve ser maior que zero")
        preco_anterior = produto.preco
        historico = HistoricoPreco (
            produto_id = produto.id,
            usuario_id = usuario_id,
            preco_anterior = preco_anterior,
            preco_novo = novo_valor
        )
        HistoricoPrecoRepository.save(historico)
        item = ProdutoRepository.update_value(produto_id, novo_valor)
        return item


  