from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from controller.filmecontroller import FilmeController
from controller.usercontroller import PessoaController
from controller.canaisController import CanaisController
from controller.comentarioController import ComentarioController

filme_bp = Blueprint("filme", __name__, template_folder="../templates")

filmeControler = FilmeController()
userControler = PessoaController()
canaisControler = CanaisController()
comentarioControler = ComentarioController()

@filme_bp.route('/gerenciamento')
def gerenciamento():
    if 'adm' not in session:
       return redirect('/')

    return render_template("gerenciamento.html")
@filme_bp.route('/filmeGerenciamento')
def filmeGerenciamento():
    if 'adm' not in session:
        return redirect('/')

    return render_template("filmes_gerenciamento.html")

@filme_bp.route('/', methods=['POST'])
def filme_gerenciamento():
    if 'adm' not in session:
        return redirect('/')

    titulo = request.form.get('titulo')
    genero = request.form.get('genero')
    categoria = request.form.get('categoria')
    data = request.form.get('data')
    descricao = request.form.get('descricao')
    canais = request.form.getlist('canais')
    foto = request.files['foto']
    video = request.files['video']
    filmeControler.adicionar_filme(titulo, genero, categoria, data, descricao, 0, foto, video, canais)
    return jsonify({"sucesso": True}), 200

    

@filme_bp.route('/<int:id>')
def filme(id):
    return render_template("filme.html")

@filme_bp.route('/getFilme/<int:id>')
def getFilme(id):
    filme_lista = filmeControler.perfil_filme(id)
    if filme_lista:
        return jsonify(filme_lista), 200
    else: 
        return jsonify({"mensagem": "Livro não encontrado"}), 404

@filme_bp.route('/listaFilmes')
def listaFilmes():
    filme_lista = filmeControler.listar_filmes()
    filme_lista_to_dict = [ c.to_dict() for c in filme_lista]
    return jsonify(filme_lista_to_dict)

@filme_bp.route('/<int:id>', methods=['PUT'])
def editar_filme(id):
    
    titulo = request.form.get('titulo-editar')
    genero = request.form.get('genero-editar')
    categoria = request.form.get('categoria-editar')
    data = request.form.get('data-editar')
    descricao = request.form.get('descricao-editar')
    canais = request.form.getlist('canais-editar')
    foto = request.files['foto-editar']
    video = request.files['video-editar']
    filmeControler.edita_filme(titulo, genero, categoria, data, descricao, foto, video, id, canais)
    return jsonify({"sucesso": True})
    

@filme_bp.route('/<int:id>', methods = ['DELETE'])
def excluir_filme(id):
    if 'logado' not in session:
        return jsonify({"mensagem": "acesso negado"})
    filmeControler.excluir_filme_controller(id)
    return jsonify({"sucesso": True})

@filme_bp.route('/filtrar', methods=['POST'])
def filtrar():
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    avaliacao_filtro = request.form.get('avaliacao_filtro')
    categoria_filtro = request.form.get('categoria_filtro')

    if filmeControler.filtrar_controller(data_inicio, data_fim, avaliacao_filtro, categoria_filtro):
        return jsonify({"sucesso": True}), 200
    
    return({"sucesso": False }), 404

@filme_bp.route('/lista_filmes_filtrados')
def lista_filmes_filtrados():
    campo = request.args.get("campo", "")  
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    avaliacao_filtro = request.args.get("avaliacao_filtro")
    categoria_filtro = request.args.get("categoria_filtro")
    print("campo", campo)
    resultado = filmeControler.filtrar_controller(data_inicio, data_fim, avaliacao_filtro, categoria_filtro, campo)
    resultado_to_dict = [c.to_dict() for c in resultado]

    return jsonify(resultado_to_dict), 200


