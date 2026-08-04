from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.models.historico_preco import HistoricoPreco
from app.repositories.historico_preco_repository import HistoricoPrecoRepository
from app.repositories.estoque_repository import EstoqueRepository
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP
from app.database import db

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
        novo_valor = Decimal(str(dados['novo_valor'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if novo_valor <= Decimal("0.00"):
            raise ValueError("O preço deve ser maior que zero")
            
        preco_anterior = Decimal(str(produto.preco))
        historico = HistoricoPreco (
            produto_id = produto.id,
            usuario_id = int(usuario_id),
            preco_anterior = preco_anterior,
            preco_novo = novo_valor
        )
        HistoricoPrecoRepository.save(historico)
        preco_atualizado = ProdutoRepository.update_value(produto_id, novo_valor)
        estoque_atualizado = EstoqueRepository.update_value(produto_id, novo_valor)
        db.session.commit()
        return {
            "produto": preco_atualizado,
            "estoques_atualizados":estoque_atualizado
        }

    @staticmethod
    def delete_produto(produto_id):
        produto = ProdutoRepository.chase_by_id(produto_id)
        if produto is None: 
            raise ValueError("Produto inválido")
        return ProdutoRepository.delete(produto.id)

  