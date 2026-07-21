from flask import Blueprint
from app.controllers.login_usuario_controller import AuthControllerUsuario

auth_bp = Blueprint("auth", __name__)

auth_bp.route(
    "/login",
    methods=["POST"]
)(AuthControllerUsuario.login)