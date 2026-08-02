from app.models.estoque import Estoque
from app.models.produto import Produto
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.unidade_repository import UnidadeRepository
from app.repositories.funcionario_repository import FuncionarioRepository

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


    @staticmethod
    def alterar_disponibilidade(usuario_id, estoque_id):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        unidade_funcionario = funcionario.unidade_id
        produto = EstoqueRepository.chase_by_id(estoque_id)
        produto_unidade = produto.id_unidade
        if unidade_funcionario != produto_unidade:
            raise ValueError("erro: sem autorização")
        is_active = produto.is_active
        if is_active == True:
            nova_atualizacao = EstoqueRepository.update_activity(produto.id, False)
        else:
            nova_atualizacao = EstoqueRepository.update_activity(produto.id, True)
        return nova_atualizacao