from flask import Blueprint, request, jsonify
from app.services.unidade_service import ServiceUnidade
from app.util.decorator_perfil import perfil_required

unidade_bp = Blueprint('unidade', __name__)

@unidade_bp.route('/admin/register/unidade', methods=['POST'])
@perfil_required("GESTAO")
def unidade_register():
    try:
        dados = request.get_json()
        unidade = ServiceUnidade.createUnidade(dados)
        return jsonify({
            "id": unidade.id,
            "cep": unidade.cep,
            "cidade": unidade.cidade,
            "estado": unidade.estado
        }), 201
    
    except ValueError as erro:
        return jsonify({"erro": str(erro)}),400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@unidade_bp.patch('/admin/<int:unidade_id>/atualize/is_active/True')
@perfil_required("GESTAO")
def atividade_true(unidade_id):
    try:
        ServiceUnidade.alterar_atividade(unidade_id, True)
        return jsonify({
            "mensagem": "Empresa agora se encontra em atividade"
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@unidade_bp.patch('/admin/<int:unidade_id>/atualize/is_active/False')
@perfil_required("GESTAO")
def atividade_false(unidade_id):
    try:
        ServiceUnidade.alterar_atividade(unidade_id, False)
        return jsonify({
            "mensagem": "Empresa agora se encontra inativa"
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400


@unidade_bp.delete('/admin/unidade/<int:unidade_id>/delete')
@perfil_required("GESTAO")
def deletar_unidade(unidade_id):
    try:
        ServiceUnidade.deletar_unidade(unidade_id)
        return jsonify({
            "mensagem":"Unidade excluida com sucesso!"
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500