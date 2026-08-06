from app.models.produto import Produto
from app.util.api_error import ApiError
from app.database import db

class ProdutoRepository:
    @staticmethod
    def save(produto: Produto):
        db.session.add(produto)
        db.session.commit()
        return produto

    @staticmethod
    def chase_by_id(produto_id: int):
        return Produto.query.get(produto_id)

    #inserir uma função de alterar dados
    @staticmethod
    def chase_by_name(nome:str):
        return Produto.query.filter_by(nome=nome).first()

    @staticmethod
    def show():
        return Produto.query.all()

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def update_value(produto_id: int, newValue: float):
        produto = Produto.query.get(produto_id)
        if produto is None:
            raise ApiError(
                error="PRODUTO_NAO_ENCONTRADO",
                message="O produto informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"produtoId",
                    "issue":f"O produto de Id {produto_id} não existe."
                }]
            )
        produto.preco = newValue
        return produto

    @staticmethod
    def get_from(produto_id: int, coluna):
        dado = db.select(coluna).where(Produto.id == produto_id)
        item = db.session.execute(dado).scalar()
        return item