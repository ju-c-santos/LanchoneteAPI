from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.database import db


cliente = Cliente(
    usuario_id = Usuario.id
)

db.session.add(cliente)
db.session.commit()