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
from app.routes.promocao_route import promocao_bp
from app.routes.docs_route import docs_bp
from uuid import uuid4
from flask import Flask, g, request
from app.util.api_error import ApiError, resposta_erro


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
    from app.models.descontos import TipoDesconto
    from app.models.promocao import Promocao
    from app.models.consentimento import Consentimento
    from app.models.fidelidade_consentimento import FidelidadeConsentimento

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
    app.register_blueprint(promocao_bp)
    app.register_blueprint(docs_bp)

    @app.before_request
    def criar_request_id():
        g.request_id = (
            request.headers.get("Request-ID") or str(uuid4())
        )

    @app.after_request
    def adicionar_request_id(response):
        response.headers["Request-ID"] = (
            g.request_id
        )
        return response

    @app.errorhandler(ApiError)
    def api_error (erro):
        return resposta_erro (
            error = erro.error,
            message = erro.message,
            status_code = erro.status_code,
            details = erro.details
        )
    
    @app.errorhandler(404)
    def rota_nao_encontrada(_erro):
        return resposta_erro(
            error = "ROTA_NAO_ENCONTRADA",
            message = "A rota solicitada não existe.",
            status_code = 404
        )

    @app.errorhandler(405)
    def metodo_nao_permitido(_erro):
        return resposta_erro(
            error = "METODO_NAO_PERMITIDO",
            message = "O método HTTP não é permitido para esta rota.",
            status_code = 405
        )

    @app.errorhandler(Exception)
    def erro_interno(erro):
        app.logger.exception(
            "Erro interno não tratado: %s",
            erro
        )
        return resposta_erro(
            error = "ERRO_INTERNO",
            message = "Ocorreu um erro interno no servior.",
            status_code = 500
        )


    return app
