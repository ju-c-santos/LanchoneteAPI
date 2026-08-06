from app.models.estoque import Estoque
from app.models.produto import Produto
from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.unidade_repository import UnidadeRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.promocao_repository import PromocaoRepository
from app.models.descontos import TipoDesconto
from decimal import Decimal, InvalidOperation
from datetime import datetime
from app.util.api_error import ApiError
from app.util.conversores import Conversores

class EstoqueService:

    @staticmethod
    def addProduto(dados):
        produto = ProdutoRepository.chase_by_id(dados['id_produto'])
        unidade_exists = UnidadeRepository.chase_by_id(dados['id_unidade'])
        if not(produto):
            raise ApiError(
                error="PRODUTO_NAO_ENCONTRADO",
                message="O produto informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"produtoId",
                    "issue":f"O produto {dados['id_produto']} não foi encontrado."
                }]
            )
        if not(unidade_exists):
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidade informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field":"unidadeId",
                    "issue":f"A unidade {dados['id_unidade']} não foi encontrada."
                }]
            )
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
    def alterar_disponibilidade(usuario_id, estoque_id, bolv):
        funcionario = FuncionarioRepository.chase_by_usuario(usuario_id)
        unidade_funcionario = funcionario.unidade_id
        produto = EstoqueRepository.chase_by_id(estoque_id)
        produto_unidade = produto.id_unidade
        if unidade_funcionario != produto_unidade:
            raise ApiError(
                error="USUARIO_NAO_AUTORIZADO",
                message="O funcionário não possui autorização.",
                status_code=403,
                details=[{
                    "field":"unidadeFuncionario",
                    "issue":"Funcionários podem alterar a disponibulidade de itens de suas respectivas unidades."
                }]
            )

        nova_atualizacao = EstoqueRepository.update_activity(produto.id, bolv)
        return nova_atualizacao

    @staticmethod
    def somar_quantidade(estoque_id, dados):
        estoque = EstoqueRepository.chase_by_id(estoque_id)
        if estoque is None:
            raise ApiError(
                error="ESTOQUE_NAO_ECONTRADO",
                message="O estoque não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"estoqueId",
                    "issue":f"O estoque com ID {estoque} informado é inexistente."
                }]
            )
        nova_quantidade = int(dados['quantidade'])
        if nova_quantidade <= 0:
            raise ApiError(
                error="QUANTIDADE_INVALIDA",
                message="A quantidade não pode ser igual ou abaixo de zero.",
                status_code=422,
                details=[{
                    "field":"nova_quantidade",
                    "issue":"A quantidade deve ser um valor acima de zero."
                }]
            )
        estoque.quantidade += nova_quantidade
        estoque.is_active = nova_quantidade > 0
        EstoqueRepository.update()
        return estoque

    @staticmethod
    def menu_cliente(unidade_id, filtros):
        ordenacoes_permitidas = {
            "nome_asc",
            "nome_desc",
            "preco_asc",
            "preco_desc"
        }
        page = filtros.get("page", 1)
        limit = filtros.get("limit", 20)
        if page is None or page < 1:
            raise ApiError(
                error="PAGINA_INVALIDA",
                message="A página deve ser maior que zero.",
                status_code=422,
                details=[{
                    "field": "page",
                    "issue": "Informe um número inteiro que seja maior que zero."
                }]
            )
        if limit is None or limit < 1 or limit > 100:
            raise ApiError(
                error="LIMITE_INVALIDO",
                message="O limite deve ser um número entre 0 e 100.",
                status_code=422,
                details=[{
                    "field": "limit",
                    "issue": "Somente são permitidos valores de 0 até 100."
                }]
            )
        nome = filtros.get("nome")
        categoria = filtros.get("categoria")
        if nome:
            nome = nome.strip()
        if categoria:
            categoria = categoria.strip()
        disponivel = Conversores.converter_booleano(filtros.get("disponivel"), campo="disponivel")
        preco_min = Conversores.converter_decimal(filtros.get("preco_min"), campo="precoMin")
        preco_max = Conversores.converter_decimal(filtros.get("preco_max"), campo="precoMax")
        if preco_min is not None and preco_max is not None and preco_min > preco_max:
            raise ApiError(
                error="INTERVALO_PRECO_INVALIDO",
                message="O preço mínimo não pode ser maior que o preço máximo.",
                status_code=422,
                details=[{
                    "field":"precoMin",
                    "issue":"Deve ser menor ou igual ao preço máximo."
                }]
            )
        ordenar = filtros.get("ordenar", "nome_asc")
        if ordenar not in ordenacoes_permitidas:
            raise ApiError(
                error="ORDENACAO_INVALIDA",
                message="A ordenação informada não é válida.",
                status_code=422,
                details=[{
                    "field":"ordenar",
                    "issue": ("Valores permitidos" + ",".join(sorted(ordenacoes_permitidas)))
                }]
            )
        paginacao = EstoqueRepository.show_menu(
            unidade_id=unidade_id,
            nome=nome,
            categoria=categoria,
            disponivel=disponivel,
            preco_min=preco_min,
            preco_max=preco_max,
            ordenar=ordenar,
            page=page,
            limit=limit
        )
        produtos = [
            EstoqueService.serializar_item_menu(estoque)
            for estoque in paginacao.items
        ]
        return {
            "quanridadeProdutos": len(produtos),
            "produtos": produtos,
            "page": paginacao.page,
            "limit": limit,
            "totalItems": paginacao.total,
            "totalPages": paginacao.pages,
            "hasNext": paginacao.has_next,
            "hasPrevious": paginacao.has_prev
        }

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