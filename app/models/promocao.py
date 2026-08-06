from datetime import datetime
from app.database import db
from app.models.descontos import TipoDesconto

class Promocao(db.Model):
    __tablename__ = 'promocoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False
    )
    unidade_id = db.Column(
        db.Integer,
        db.ForeignKey("unidade.id", ondelete="CASCADE"),
        nullable=True
    )
    tipo_desconto = db.Column(db.Enum(TipoDesconto), nullable=False)
    valor_desconto = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_minima = db.Column(db.Integer, default=1, nullable=False)
    data_inicio = db.Column(db.DateTime,nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    ativa = db.Column(db.Boolean, default=True, nullable=False)

    produtos = db.relationship(
        "Produto",
        back_populates="promocoes"
    )

    unidade = db.relationship(
        "Unidade",
        back_populates="promocoes"
    )    

    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "produtoId": self.produto_id,
            "unidadeId": self.unidade_id,
            "tipoDesconto": self.tipo_desconto,
            "quantidadeMinima": self.quantidade_minima,
            "dataInicio": self.data_inicio.isoformat(),
            "dataFim": self.data_fim.isoformat(),
            "ativa": self.ativa
        }