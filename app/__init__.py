from flask import Flask
from flask_jwt_extended import JWTManager
from app.database import db, migrate
from app.routes.login_route import auth_bp
from app.routes.usuarios_routes import usuario_bp
from app.routes.register_funcionario_route import funcionario_bp
from app.routes.register_admin_route import admin_bp
from app.routes.unidade_register_route import unidade_bp
from app.routes.estoque_route import estoque_bp
from app.routes.produto_route import produto_bp
from app.routes.pedidos_route import pedido_bp
from app.routes.pagamento_route import pagamento_bp



jwt = JWTManager()

def create_app():
    from app.models.pontos import Pontos
    from app.models.funcionario import Funcionario
    from app.models.usuario import Usuario
    from app.models.unidade import Unidade
    from app.models.perfil import Perfil
    from app.models.cliente import Cliente
    from app.models.estoque import Estoque
    from app.models.produto import Produto
    from app.models.metodo_pagamento import MetodoPagamento
    from app.models.status import Status
    from app.models.item_pedido import ItemPedido
    from app.models.pedido import Pedido
    from app.models.pagamento import Pagamento
    from app.models.local_pedido import LocalPedido
    from app.models.historico_preco import HistoricoPreco

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(funcionario_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(unidade_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(pagamento_bp)

    return app
