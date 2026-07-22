from flask import request, jsonify
from app.services.usuario_service import AuthServiceUsuario

class AuthControllerUsuario:
    
    @staticmethod
    def login():
        try:
            dados = request.get_json()
            token = AuthServiceUsuario.login(
                dados["user"],
                dados["senha"]
            )
            return jsonify({
                "access_token": token
            }), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 401