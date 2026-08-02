from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository

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
    def alterarValor(produto_id, dados):
        produto = ProdutoRepository.chase_by_id(produto_id)
        if produto is None: 
            raise ValueError("Produto não encontrado")
        novo_valor = float(dados['novo_valor'])
        item = ProdutoRepository.update_value(produto_id, novo_valor)
        return item
