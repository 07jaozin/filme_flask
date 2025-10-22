from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from controller.canaisController import CanaisController
from controller.usercontroller import PessoaController

canais_bp = Blueprint("canais", __name__, template_folder="../templates")

canaisControler = CanaisController()
userControler = PessoaController()



@canais_bp.route('/')
def pagCanais():
    return render_template("canais.html")

@canais_bp.route('/getCanais')
def getCanais():
    canais_lista = canaisControler.listar_canais()
    canais_dic = [c.to_dict() for c in canais_lista]

    return jsonify(canais_dic)

@canais_bp.route('/getCanal/<int:id>')
def getCanal(id):
    canais_lista = canaisControler.buscar_por_idCanal(id)
    canais_dic = canais_lista.to_dict()

    return jsonify(canais_dic), 200

@canais_bp.route('/buscar_canal_id/<int:id>')
def buscar_canal_id(id):
    canal = canaisControler.buscar_por_id(id)
    print(canal)
    canais_to_dict = [c.to_dict() for c in canal]
    print(canais_to_dict)
    if canal :
        return jsonify(canais_to_dict), 200
    return jsonify("erro"), 200

@canais_bp.route('/', methods=['POST'])
def canais():
    if 'adm' not in session:
        return render_template("erro.html")
    if request.method == 'POST':
        nome = request.form.get('nome_canal')
        link = request.form.get('link_canal')
        foto = request.files['foto_canal']
        canaisControler.adicionar_canal(nome, link, foto)
        return jsonify({"sucesso": True})
    else:
        return render_template("canais.html")

@canais_bp.route('/<int:id>', methods = ['DELETE'])
def excluir_canal(id):
    if 'adm' not in session:
        return render_template("erro.html")
    if canaisControler.deletar_canal(id):
        return jsonify({"sucesso": True})
    else: 
        return jsonify({"sucesso": False})

@canais_bp.route('/<int:id>', methods=['PUT'])
def editar_canais(id):
    if 'adm' not in session:
        return jsonify({"sucesso": False}), 200
    
    nome = request.form.get('nome_canal-editar')
    link = request.form.get('link_canal-editar')
    foto = request.files['foto_canal-editar']
    if canaisControler.editar_canal(id, nome, link, foto):
        return jsonify({"sucesso": True})
    return jsonify({"sucesso": False})

    

   
