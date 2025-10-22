from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from controller.comentarioController import ComentarioController
from controller.usercontroller import PessoaController
from controller.filmecontroller import FilmeController

comentario_bp = Blueprint("comentario", __name__, template_folder="../templates")

comentarioControler = ComentarioController()
userControler = PessoaController()
filmeControler = FilmeController()

@comentario_bp.route('/<int:id>')
def lista(id):
    lista_comentarios = comentarioControler.listar_comentarios_filme(id)

    if lista_comentarios != []:
        return jsonify(lista_comentarios)
    
    else:
        return jsonify("nenhum"), 200
    
    


@comentario_bp.route('/<int:id>', methods=['POST'])
def comentarios(id):
    if 'logado' not in session:
        
        return jsonify({"mensagem": "acesso negado"}), 404

    id_usuario = session['id']
    comentario = request.form.get('comentario')
    avaliacao = int(request.form.get('avaliacao-comentarios'))
    print(comentario)
    print(avaliacao)
    if comentarioControler.inserir_comentario_controller(comentario, avaliacao, id_usuario, id):
        return jsonify({"sucesso": True}), 200
    return jsonify({"sucesso": False}), 404
    

@comentario_bp.route('/<int:id>/<int:id_filme>', methods=['DELETE'])
def excluir_comentarios(id, id_filme):
    if comentarioControler.excluir_comen(id, id_filme):
        return jsonify({"sucesso": True}), 200
    return jsonify({"sucesso": False}), 404

@comentario_bp.route('/<int:id>/<int:id_filme>', methods=['PUT'])
def editar_comentario(id, id_filme):
    if 'id' not in session:
        return jsonify({"mensagem": "acesso negado"}), 404
    
    comentario = request.form.get('comentario-editar')
    avaliacao = float(request.form.get('avaliacao-editar'))

    if comentarioControler.editar_comen(comentario, avaliacao, id, id_filme):
        return jsonify({"sucesso": True}), 200
    
    return jsonify({"sucesso": False}), 404
    
