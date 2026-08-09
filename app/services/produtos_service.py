from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.models.historico_preco import HistoricoPreco
from app.repositories.historico_preco_repository import HistoricoPrecoRepository
from app.repositories.estoque_repository import EstoqueRepository
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP
from app.database import db
from app.util.api_error import ApiError
from app.util.conversores import Conversores

class ProdutoService:

    @staticmethod
    def novoProduto(dados):
        produto_exists = ProdutoRepository.chase_by_name(dados['nome'])
        if produto_exists:
            raise ApiError(
                error="PROTUDO_EXISTENTE",
                message="O produto já está cadastrado.",
                status_code=409,
                details=[{
                    "field":"nome",
                    "issue":f"O produto {dados["nome"]} já consta cadastrado no sistema."
                }]

            )
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
            raise ApiError(
                error="PRODUTO_NAO_ENCONTRADO",
                message="O produto informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"produtoId",
                    "issue":f"O produto {produto_id} não existe."
                }]
            )
        novo_valor = Decimal(str(dados['novoValor'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if novo_valor <= Decimal("0.00"):
            raise ApiError(
                error="VALOR_INVALIDO",
                message="O preço deve ser maior ou igual a zero.",
                status_code=422,
                details=[{
                    "field":"novoValor",
                    "issue":"O campo novo_valor não pode ser um número negativo."
                }]
            ) 
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
            "estoquesAtualizados":estoque_atualizado
        }

    @staticmethod
    def listar_preco_filtrado(filtros):
        ordenacoes_permitidas ={
            "nome_asc",
            "nome_desc",
            "categoria_asc",
            "categoria_desc",
            "produtoId_asc",
            "produtoId_desc"
        }
        page = filtros.get("page", 1)
        limit = filtros.get("limit", 20)
        if page is None or page < 1:
            raise ApiError(
                error="PAGINA_INVALIDA",
                message="A página deve ser maior que zero.",
                status_code=422,
                details=[{
                    "field":"page",
                    "issue":"Informe um número que seja maior que zero."
                }]
            )
        if limit is None or 1 > limit or limit > 100:
            raise ApiError(
                error="LIMITE_INVALIDO",
                message="O limite deve ser um número entre 1 e 100.",
                status_code=422,
                details=[{
                    "field":"limit",
                    "issue":"Valores permitidos: 1 até 100."
                }]
            )
        produto_id = Conversores.converter_id(filtros.get("produto_id"), campo="produtoId")
        nome = filtros.get("nome")
        if nome:
            nome = nome.strip()
        categoria = filtros.get("categoria")
        if categoria:
            categoria = categoria.strip()
        data_inicio = Conversores.converter_data(filtros.get("data_inicio"), campo="dataInicio", fim_do_dia=False)
        data_fim = Conversores.converter_data(filtros.get("data_fim"), campo="dataFim", fim_do_dia=True)
        if data_inicio is not None and data_fim is not None and data_inicio > data_fim:
            raise ApiError(
                error="PERIODO_INVALIDO",
                message="A data de inicio não pode ser depois da data de fim.",
                status_code=422,
                details=[{
                    "field":"dataInicio",
                    "issue":"Deve ser antes da data final."
                }]
            )
        valor_novo_min = Conversores.converter_decimal(filtros.get("valor_novo_min"), campo="valorNovoMin")
        valor_novo_max = Conversores.converter_decimal(filtros.get("valor_novo_max"), campo="valorNovoMax")
        if valor_novo_min is not None and valor_novo_max is not None and valor_novo_min > valor_novo_max:
            raise ApiError(
                error="INTERVALO_INVALIDO",
                message="O valor mínimo deve ser menor ou igual ao valor máximo.",
                status_code=422,
                details=[{
                    "field":"valorNovoMin",
                    "issue":"Deve ser menor ou igual ao valor máximo."
                }]
            )
        ordenar = filtros.get("ordenar", "produtoId_desc")
        if ordenar not in ordenacoes_permitidas:
            raise ApiError(
                error="ORDENACAO_INVALIDA",
                message="A ordenação informada é inváida.",
                status_code=422,
                details=[{
                    "field":"ordenar",
                    "issue":"Valores permitidos: "+", ".join(ordenacoes_permitidas)
                }]
            )
        paginacao = (HistoricoPrecoRepository.listar_recentes(
            produto_id=produto_id, 
            nome=nome, 
            categoria=categoria, 
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            valor_novo_min=valor_novo_min,
            valor_novo_max=valor_novo_max, 
            ordenar=ordenar, 
            page=page, 
            limit=limit))
        return {
            "historico":[
                registro.to_dict()
                for registro in paginacao.items                
            ],
            "meta": {
                "page": paginacao.page,
                "limit": limit,
                "totalItems": paginacao.total,
                "totalPages": paginacao.pages,
                "hasNext": paginacao.has_next,
                "hasPrevious": paginacao.has_prev
            }
        } 

