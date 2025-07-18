from flask import Flask, request, redirect, flash, render_template, session, jsonify
from model.pessoas import Pessoas
from controller.filmecontroller import FilmeController
from controller.usercontroller import PessoaController
from controller.comentarioController import ComentarioController
from controller.canaisController import CanaisController
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)
userControler = PessoaController()
filmeControler = FilmeController()
comentarioControler = ComentarioController()
canaisControler = CanaisController()

@app.route('/')
def principal():
    
    
    if 'id' in session:
        usuario = userControler.perfil(session['id'])
    else:
        usuario = ''

    if not usuario:
        usuario = ''
    print('usuario = ', usuario)
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
     tipo = 'normal'

     userControler.adicionar_pessoa(nome, senha, foto, tipo)

     return redirect('/login')

@app.route('/gerenciamento', methods = ['POST', 'GET'])
def gerenciamento():
    if 'adm' not in session:
        flash("Desculpe-me, mas voce não tem permissão de acessar esta pagina")
        return render_template("erro.html")
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        genero = request.form.get('genero')
        categoria = request.form.get('categoria')
        data = request.form.get('data')
        descricao = request.form.get('descricao')
        canais = request.form.getlist('canais')
        foto = request.files['foto']
        video = request.files['video']
        filmeControler.adicionar_filme(titulo, genero, categoria, data, descricao, 0, foto, video, canais)
        return redirect('/gerenciamento')


    else:
        usuario = userControler.perfil(session['id'])
        filmes = filmeControler.listar_filmes()
        canais = canaisControler.listar_canais()
        return render_template("gerenciamento.html", filmes = filmes, usuario = usuario, canais = canais)

@app.route('/filme_gerenciamento', methods = ['GET', 'POST'])
def filme_gerenciamento():
    if 'adm' not in session:
        flash("Desculpe-me, mas voce não tem permissão de acessar esta pagina")
        return render_template("erro.html")
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        genero = request.form.get('genero')
        categoria = request.form.get('categoria')
        data = request.form.get('data')
        descricao = request.form.get('descricao')
        canais = request.form.getlist('canais')
        foto = request.files['foto']
        video = request.files['video']
        filmeControler.adicionar_filme(titulo, genero, categoria, data, descricao, 0, foto, video, canais)
        return redirect('/filme_gerenciamento')


    else:
        usuario = userControler.perfil(session['id'])
        filmes = filmeControler.listar_filmes()
        canais_lista = canaisControler.listar_canais()

       
        return render_template("filmes_gerenciamento.html", filmes = filmes, usuario = usuario, canais_lista = canais_lista)
@app.route('/filme/<int:id>')
def filme(id):
    
    perfil = filmeControler.perfil_filme(id)
    comentarios = comentarioControler.listar_comentarios_filme(id)
    if 'id' in session:
        usuario = userControler.perfil(session['id'])
    else:
        usuario = ''

    return render_template("filme.html", perfil = perfil, usuario = usuario, comentarios = comentarios)

@app.route('/pesquisa', methods = ['POST', 'GET'])
def pesquisa():
    
    if 'primeira_vez' not in session:
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
    if 'id' in session:
        usuario = userControler.perfil(session['id'])
    else:
        usuario = ''
    return render_template("pesquisa.html", usuario = usuario, filmes = filmes, pesquisa_campo = pesquisa_campo)

@app.route('/logout')
def logout():
    if 'logado' not in session:
      return redirect('/formulario')
    session.pop('primeira_vez', default=None)
    session.pop('logado', default=None)
    session.pop('id', default=None)
    session.pop('adm', default=None)
    return redirect('/')

@app.route('/editar_filme/<int:id>', methods = ['POST', 'GET'])
def edita_filme(id):
    if 'logado' not in session:
        return redirect('/login')
    if request.method == 'POST':
        titulo = request.form.get('titulo-editar')
        genero = request.form.get('genero-editar')
        categoria = request.form.get('categoria-editar')
        data = request.form.get('data-editar')
        descricao = request.form.get('descricao-editar')
        canais = request.form.getlist('canais-editar')
        foto = request.files['foto-editar']
        video = request.files['video-editar']
        filmeControler.edita_filme(titulo, genero, categoria, data, descricao, foto, video, id, canais)
        print(canais)
        return redirect('/filme_gerenciamento')
    else:
        filme = filmeControler.perfil_filme(id)
        canais_lista = canaisControler.listar_canais()
        usuario = userControler.perfil(session['id'])

        print(filme['canais'])
        for c1 in filme['canais']:
            for c2 in canais_lista:
                
                if c1[0] == c2.id:
                    
                    c2.checked = "checked"

        return render_template("editar.html", filme = filme, canais_lista = canais_lista, usuario = usuario)
@app.route('/excluir_fime/<int:id>')
def excluir_filme(id):
    if 'logado' not in session:
        return redirect('/login')
    filmeControler.excluir_filme_controller(id)
    return redirect('/filme_gerenciamento')

@app.route('/perfil_usuario/<int:id>', methods = ['GET', 'POST'])
def perfil_usuario(id):
    if 'logado' not in session:
        return redirect('/login')
    else:
        usuario = userControler.perfil(id)
        return render_template("perfil.html", usuario = usuario)
@app.route('/excluir_perfil/<int:id>')
def excluir_perfil(id):
    if 'logado' not in session:
        return redirect('/')
    session.pop('primeira_vez', default=None)
    session.pop('logado', default=None)
    session.pop('id', default=None)
    comentarioControler.delete_comentario_controller(id)
    userControler.excluir_usuario_controler(id)
    return redirect('/')

@app.route('/editar_perfil/<int:id>', methods = ['GET', 'POST'])
def editar_perfil(id):
     if 'logado' not in session:
        return redirect('/login')
     if request.method == 'POST':
        nome = request.form.get('nome-editar')
        senha = request.form.get('senha-editar')
        foto = request.files['foto-editar']

        userControler.edita_pessoa(id, nome, senha, foto)
        return redirect(f'/perfil_usuario/{id}')
     
     else:
         usuario = userControler.perfil(id)
         return render_template("editar_usuario.html", usuario = usuario)

@app.route('/deletar_foto_perfil') 
def deletar_foto_perfil():
    if 'logado' not in session:
        return redirect('/login')
    id = session['id']
    if userControler.remover_foto(id):
        return redirect(f'/perfil_usuario/{id}')
    return "erro", 404

@app.route('/comentarios/<int:id>', methods = ['POST', 'GET'])
def comentarios(id):
    if 'logado' not in session:
        flash("Desculpe-me, mas voce não tem permissão de acessar esta pagina, por favor se cadastre para poder comentar")
        return render_template("erro.html")
    if 'id' in session:
        usuario = userControler.perfil(session['id'])
    else:
        usuario = ''

    if not usuario:
        usuario = ''
    
    if request.method == 'POST':
    
        id_usuario = session['id']
        comentario = request.form.get('comentario')
        avaliacao = float(request.form.get('avaliacao-comentarios'))


        if comentarioControler.inserir_comentario_controller(comentario, avaliacao, id_usuario, id):
            return redirect(f'/filme/{id}')

        else:
            return "erro", 404
        
    else:

        filme = filmeControler.perfil_filme(id)

        return render_template("comentar.html", filme = filme, usuario = usuario)

@app.route('/excluir_comentario/<int:id>/<int:id_filme>', methods = ['POST'])
def excluir_comentarios(id, id_filme):
    if comentarioControler.excluir_comen(id, id_filme):
        return redirect(f'/filme/{id_filme}')
    
    return "erro", 404

@app.route('/editar_comentario/<int:id>/<int:id_filme>', methods = ['POST', 'GET'])
def editar_comentario(id, id_filme):
    if 'id' in session:
        usuario = userControler.perfil(session['id'])
    else:
        usuario = ''

    if not usuario:
        usuario = ''

    if request.method == 'POST':
        comentario = request.form.get('comentario-editar')
        avaliacao = float(request.form.get('avaliacao-editar'))
        print(avaliacao)

        if comentarioControler.editar_comen(comentario, avaliacao, id, id_filme):
            return redirect(f'/filme/{id_filme}')
        
        return "erro", 404
    
    else:
        comentario = comentarioControler.comentario_espe(id)
        filmes = filmeControler.perfil_filme(id_filme)
        return render_template("editar_comentario.html", c = comentario, filmes = filmes, usuario = usuario)

@app.route('/filtrar', methods = ['POST'])
def filtrar():
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    avaliacao_filtro = request.form.get('avaliacao_filtro')
    categoria_filtro = request.form.get('categoria_filtro')
    print("data ", data_inicio)

    if filmeControler.filtrar_controller(data_inicio, data_fim, avaliacao_filtro, categoria_filtro):
        return redirect('/pesquisa')
    
    return "erro", 404

@app.route('/canais', methods = ['GET', 'POST'])
def canais():
    if 'adm' not in session:
        flash("Desculpe-me, mas voce não tem permissão de acessar esta pagina")
        return render_template("erro.html")
    if request.method == 'POST':
        nome = request.form.get('nome_canal')
        link = request.form.get('link_canal')
        foto = request.files['foto_canal']
        canaisControler.adicionar_canal(nome, link, foto)

        return redirect('/canais')
    
    else:
        canais_lista = canaisControler.listar_canais()
        usuario = userControler.perfil(session['id'])
        return render_template("canais.html", canais_lista = canais_lista, usuario = usuario)
    
@app.route('/excluir_canal/<int:id>')
def excluir_canal(id):
    if 'adm' not in session:
        flash("Desculpe-me, mas voce não tem permissão de acessar esta pagina")
        return render_template("erro.html")
    canaisControler.deletar_canal(id)
    return redirect('/canais')
@app.route('/editar_canais/<int:id>', methods = ['GET', 'POST'])
def editar_canais(id):
    if 'adm' not in session:
        flash("Desculpe-me, mas voce não tem permissão de acessar esta pagina")
        return render_template("erro.html")
    if request.method == 'POST':
        nome = request.form.get('nome_canal-editar')
        link = request.form.get('link_canal-editar')
        foto = request.files['foto_canal-editar']
        canaisControler.editar_canal(id, nome, link, foto)

        return redirect('/canais')
    else:
        canais_lista = canaisControler.buscar_por_id(id)
        usuario = userControler.perfil(session['id'])
        return render_template("editar_canais.html", canal = canais_lista, usuario = usuario)
