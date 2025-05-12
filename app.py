from flask import Flask, request, redirect, flash, render_template, session
from model.pessoas import Pessoas
from controller.filmecontroller import FilmeController
from controller.usercontroller import PessoaController
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)
userControler = PessoaController()
filmeControler = FilmeController()

@app.route('/')
def principal():
    if 'logado' not in session:
        return redirect('/login')
    print(session['id'])
    usuario = userControler.perfil(session['id'])
    print(usuario)
    filmes = filmeControler.listar_filmes()

    return render_template("index.html", usuario = usuario, filmes = filmes)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        if userControler.verificação(nome, senha):
            return redirect('/')
        else:
            return redirect('/login')
        
    else:
        return render_template("login.html")

@app.route('/cadastro', methods = ['POST'])
def cadastrar():
     nome = request.form.get('nome-cadastrar')
     senha = request.form.get('senha-cadastrar')
     foto = request.files['foto-cadastrar']

     userControler.adicionar_pessoa(nome, senha, foto)

     return redirect('/login')

@app.route('/gerenciamento', methods = ['POST', 'GET'])
def gerenciamento():
    if 'logado' not in session:
        return redirect('/login')
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        genero = request.form.get('genero')
        categoria = request.form.get('categoria')
        data = request.form.get('data')
        foto = request.files['foto']
        video = request.files['video']
        filmeControler.adicionar_filme(titulo, genero, categoria, data, foto, video)
        return redirect('/gerenciamento')


    else:
        usuario = userControler.perfil(session['id'])
        filmes = filmeControler.listar_filmes()
        return render_template("gerenciamento.html", filmes = filmes, usuario = usuario)

@app.route('/filme/<int:id>')
def filme(id):
    if 'logado' not in session:
        return redirect('/login')
    perfil = filmeControler.perfil_filme(id)
    usuario = userControler.perfil(session['id'])

    return render_template("filme.html", perfil = perfil, usuario = usuario)

@app.route('/pesquisa', methods = ['POST', 'GET'])
def pesquisa():
    if 'logado' not in session:
        return redirect('/login')
    elif 'primeira_vez' not in session:
        print('aq')
        filmes = filmeControler.listar_filmes()
        pesquisa_campo = ''
    else:
        filmes = filmeControler.listar_pesquisa
        pesquisa_campo = filmeControler.campo_pesquisa

    if request.method == 'POST':
        campo = request.form.get('campo')
        filmes = filmeControler.pesquisar_filme(campo)
        return redirect('/pesquisa')
    
    print("pesquisa: ", filmes)
    usuario = userControler.perfil(session['id'])
    return render_template("pesquisa.html", usuario = usuario, filmes = filmes, pesquisa_campo = pesquisa_campo)

@app.route('/logout')
def logout():
    if 'logado' not in session:
      return redirect('/formulario')
    session.pop('primeira_vez', default=None)
    session.pop('logado', default=None)
    session.pop('id', default=None)
    return redirect('/login')

@app.route('/editar_filme/<int:id>', methods = ['POST', 'GET'])
def edita_filme(id):
    if request.method == 'POST':
        titulo = request.form.get('titulo-editar')
        genero = request.form.get('genero-editar')
        categoria = request.form.get('categoria-editar')
        data = request.form.get('data-editar')
        foto = request.files['foto-editar']
        video = request.files['video-editar']
        filmeControler.edita_filme(titulo, genero, categoria, data, foto, video, id)
        return redirect('/gerenciamento')
    else:
        filme = filmeControler.perfil_filme(id)
        return render_template("editar.html", filme = filme)
@app.route('/excluir_fime/<int:id>')
def excluir_filme(id):
    filmeControler.excluir_filme_controller(id)
    return redirect('/gerenciamento')

@app.route('/perfil_usuario/<int:id>', methods = ['GET', 'POST'])
def perfil_usuario(id):
    if request.method == 'POST':
        nome = request.form.get('nome-editar')
        senha = request.form.get('senha-editar')
        foto = request.files('foto-editar')

        userControler.edita_pessoa(id)
        return redirect(f'/perfil_usuario/{id}')
    else:
        usuario = userControler.perfil(id)
        return render_template("perfil.html", usuario = usuario)
@app.route('/excluir_perfil/<int:id>')
def excluir_perfil(id):
    session.pop('primeira_vez', default=None)
    session.pop('logado', default=None)
    session.pop('id', default=None)
    userControler.excluir_usuario_controler(id)
    return redirect('/login')

@app.route('/editar_perfil/<int:id>', methods = ['GET', 'POST'])
def editar_perfil(id):
     if request.method == 'POST':
        nome = request.form.get('nome-editar')
        senha = request.form.get('senha-editar')
        foto = request.files['foto-editar']

        userControler.edita_pessoa(id, nome, senha, foto)
        return redirect(f'/perfil_usuario/{id}')
     
     else:
         usuario = userControler.perfil(id)
         return render_template("editar_usuario.html", usuario = usuario)