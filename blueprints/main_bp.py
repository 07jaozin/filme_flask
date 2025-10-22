from flask import Blueprint, render_template, session, redirect, request, flash, jsonify
from controller.usercontroller import PessoaController
from controller.filmecontroller import FilmeController
from controller.canaisController import CanaisController

main_bp = Blueprint("main", __name__, template_folder="../templates")

userControler = PessoaController()
filmeControler = FilmeController()
canaisControler = CanaisController()

@main_bp.route('/')
def principal():
    return render_template("index.html")

@main_bp.route('/pesquisa', methods=['POST'])
def pesquisa_post():
    
    campo = request.form.get('campo')
    filmes = filmeControler.pesquisar_filme(campo)
    return jsonify({"sucesso": True}), 200

@main_bp.route('/pesquisa')
def pesquisa():
    
    return render_template("pesquisa.html")

   

@main_bp.route('/logout')
def logout():
    session.pop('primeira_vez', None)
    session.pop('logado', None)
    session.pop('id', None)
    session.pop('adm', None)
    return redirect('/')
