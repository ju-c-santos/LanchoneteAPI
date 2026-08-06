from app.database import db
from app.models.historico_preco import HistoricoPreco
from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from sqlalchemy import func


class HistoricoPrecoRepository:

    @staticmethod
    def save(registro):
        db.session.add(registro)
        return registro

    #listar alterações de preco do dia
    @staticmethod
    def listar_recentes(
        produto_id=None, nome=None, categoria=None, data_inicio=None, data_fim=None,
        valor_novo_min=None, valor_novo_max=None, ordenar="produtoId_desc", page=1, limit=20
    ):
        query = HistoricoPreco.query
        if produto_id is not None:
            query = query.filter(HistoricoPreco.produto_id == produto_id)
        if nome is not None:
            query = query.filter(Produto.nome.ilike(f"%{nome}%"))
        if categoria is not None:
            query = query.filter(Produto.categoria.ilike(f"%{categoria}%"))
        if data_inicio is not None:
            query = query.filter(HistoricoPreco.data_alteracao >= data_inicio) 
        if data_fim is not None:
            query = query.filter(HistoricoPreco.data_alteracao <= data_fim)
        if valor_novo_min is not None:
            query = query.filter(HistoricoPreco.preco_novo >= valor_novo_min)
        if valor_novo_max is not None:
            query = query.filter(HistoricoPreco.preco_novo <= valor_novo_max)  
        ordenacoes={
            "nome_asc": func.lower(Produto.nome).asc(),
            "nome_desc": func.lower(Produto.nome).desc(),
            "categoria_asc": func.lower(Produto.categoria).asc(),
            "categoria_desc": func.lower(Produto.categoria).desc(),
            "produtoId_asc": HistoricoPreco.produto_id.asc(),
            "produtoId_desc": HistoricoPreco.produto_id.desc()
        }
        query = query.order_by(ordenacoes[ordenar])
        return query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
