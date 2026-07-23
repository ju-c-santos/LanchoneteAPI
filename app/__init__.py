from flask import Flask
from flask_jwt_extended import JWTManager
from app.database import db, migrate
from app.routes.login_route import auth_bp
from app.routes.usuarios_routes import usuario_bp
from app.routes.register_funcionario_route import funcionario_bp
from app.routes.register_admin_route import admin_bp

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models.funcionario import Funcionario
    from app.models.usuario import Usuario
    from app.models.unidade import Unidade
    from app.models.perfil import Perfil
    from app.models.cliente import Cliente

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(funcionario_bp)
    app.register_blueprint(admin_bp)

    return app
