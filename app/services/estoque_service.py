from app.models.estoque import Estoque
from app.models.produto import Produto
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.unidade_repository import UnidadeRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.promocao_repository import PromocaoRepository
from app.models.descontos import TipoDesconto
from decimal import Decimal
from datetime import datetime

class EstoqueService:

    @staticmethod
    def addProduto(dados):
        produto = ProdutoRepository.chase_by_id(dados['id_produto'])
        unidade_exists = UnidadeRepository.chase_by_id(dados['id_unidade'])
        if not(produto):
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
        item = EstoqueRepository.save(estoque)
        if estoque.is_active == False:
            EstoqueRepository.update_activity(estoque.id, True)
        return item

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

    @staticmethod
    def somar_quantidade(estoque_id, dados):
        estoque = EstoqueRepository.chase_by_id(estoque_id)
        if estoque is None:
            raise ValueError("Item inválido")
        nova_quantidade = int(dados['quantidade'])
        if nova_quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa")
        estoque.quantidade += nova_quantidade
        estoque.is_active = nova_quantidade > 0
        EstoqueRepository.update()
        return estoque

    @staticmethod
    def menu_cliente(unidade_id):
        estoques = EstoqueRepository.show_menu(unidade_id)
        return [
            EstoqueService.serializar_item_menu(estoque)
            for estoque in estoques
        ]

    @staticmethod
    def serializar_item_menu(estoque):
        promocao = PromocaoRepository.chase_by_produto(estoque.id_produto, estoque.id_unidade)
        preco_original = Decimal(str(estoque.preco))
        preco_final = preco_original
        dados_promocao = None
        if promocao is not None:
            agora = datetime.now()
            if(promocao.ativa and promocao.data_inicio <= agora <= promocao.data_fim):
                desconto = Decimal(str(promocao.valor_desconto))
                if promocao.tipo_desconto == TipoDesconto.PERCENTUAL:
                    preco_final = preco_original * (Decimal("1") - desconto / Decimal("100"))
                elif promocao.tipo_desconto == TipoDesconto.VALOR_FIXO:
                    preco_final = preco_original - desconto
                if preco_final < Decimal("0.00"):
                    preco_final = Decimal("0.00")
                dados_promocao = {
                    "id": promocao.id,
                    "nome": promocao.nome,
                    "tipo": promocao.tipo_desconto.value,
                    "valor": float(promocao.valor_desconto),
                    "quantidade_minima": promocao.quantidade_minima,
                    "data_fim": promocao.data_fim.isoformat()
                }
        return {
            "estoque_id": estoque.id,
            "produto_id": estoque.id_produto,
            "unidade_id": estoque.id_unidade,
            "nome": estoque.produtos.nome,
            "descricao": estoque.produtos.descricao,
            "categoria": estoque.produtos.categoria,
            "quantidade_disponivel": estoque.quantidade,
            "preco_original": float(preco_original),
            "preco_promocional": float(preco_final.quantize(Decimal("0.01"))),
            "promocao": dados_promocao
        }