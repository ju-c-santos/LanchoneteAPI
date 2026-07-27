from app.models.estoque import Estoque
from app.models.produto import Produto
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.unidade_repository import UnidadeRepository

class EstoqueService:

    @staticmethod
    def addProduto(dados):
        produto_exists = ProdutoRepository.chase_by_id(dados['id_produto'])
        unidade_exists = UnidadeRepository.chase_by_id(dados['id_unidade'])
        if not(produto_exists):
            raise ValueError("Produto inexistente")
        if not(unidade_exists):
            raise ValueError("Unidade inexistente")
        categoria = ProdutoRepository.get_from(dados['id_produto'], Produto.categoria)
        preco = ProdutoRepository.get_from(dados['id_produto'], Produto.preco)
        estoque = Estoque(
            id_produto = dados['id_produto'],
            id_unidade = dados['id_unidade'],
            quantidade = dados['quantidade'],
            categoria = categoria,
            preco = preco
        )
        return EstoqueRepository.save(estoque)