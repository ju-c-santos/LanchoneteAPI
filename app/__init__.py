from flask import Flask
from flask_jwt_extended import JWTManager
#from flask_cors import CORS
from app.database import db, migrate

jwt = JWTManager()

def create_app():
    from app.models.usuario import Usuario
    from app.routes.login_route import auth_bp

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    #CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    #jwt.init_app(app)
    
    #from app.routes.home_route import home
    #app.register_blueprint(home)

    app.register_blueprint(auth_bp)

    return app
