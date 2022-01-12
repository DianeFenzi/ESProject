from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user
from imdb import db, login_required, admin_required
from imdb.filme.models import Filme, Avaliacao


filme = Blueprint('filme', __name__, template_folder='templates')

################################################
#####              BLUEPRINT               #####
################################################

@filme.route("/", methods=["GET", "POST"])
def lista():
    filmes = []
    busca = False
    if request.method == "POST":
        busca = request.form.get("busca")
        filmes += Filme.query.filter(Filme.titulo.like(f"%{busca}%"))
        filmes += Filme.query.filter(Filme.id_imdb.like(f"%{busca}%"))
        filmes += Filme.query.filter(Filme.diretor.like(f"%{busca}%"))
        filmes += Filme.query.filter(Filme.atores.like(f"%{busca}%"))
        filmes = set(list(filmes))
    else:
        filmes = Filme.query.all()
    return render_template("lista.html.j2", filmes=filmes, busca=busca)

@filme.route("/<id_filme>/")
def visualizar(id_filme):
    filme = Filme.query.get_or_404(id_filme)
    comentarios = Avaliacao.query.filter(Avaliacao.id_filme==id_filme)
    return render_template("visualizar.html.j2", filme=filme, comentarios=comentarios)

@filme.route("/adicionar/", methods=["GET", "POST"])
@admin_required()
def adicionar():
    if request.method == "GET":
        return render_template("adicionar.html.j2")
    if request.method == "POST":
        titulo = request.form.get('titulo')
        imdb_id = request.form.get('imdb_id')
        diretor = request.form.get('diretor')
        atores = request.form.get('atores')
        if ', ' in atores:
            atores = ','.join(atores.split(', '))
        filme = Filme(titulo, imdb_id, diretor, atores)
        db.session.add(filme)
        db.session.commit()
        flash("Filme adicionado com sucesso")
        return redirect(url_for('filme.adicionar'))

@filme.route("/editar/<filme_id>", methods=["GET", "POST"])
@admin_required()
def editar(filme_id):
    if request.method == "GET":
        filme = Filme.query.get_or_404(filme_id)
        return render_template("editar.html.j2", filme=filme)
    if request.method == "POST":
        filme = Filme.query.get(request.form.get('id'))
        filme.titulo = request.form.get('titulo')
        filme.imdb_id = request.form.get('imdb_id')
        filme.diretor = request.form.get('diretor')
        atores = request.form.get('atores')
        if ', ' in atores:
            atores = ','.join(atores.split(', '))
        filme.atores = atores
        db.session.commit()
        flash("Filme editado com sucesso")
        return redirect(url_for('filme.editar', filme_id=filme.id))

@filme.route("/remover/<filme_id>")
@admin_required()
def remover(filme_id):
    filme = Filme.query.get(filme_id)
    db.session.delete(filme)
    db.session.commit()
    flash("Filme removido com sucesso")
    return redirect(url_for('filme.lista'))


################################################


@filme.route("<id_filme>/avaliar", methods=["GET", "POST"])
@login_required()
def avaliar(id_filme):
    id_usuario = current_user.id
    if request.method == "GET":
        if len(Avaliacao.query.filter_by(id_usuario = id_usuario, id_filme=id_filme).all()) == 0:
            return render_template("avaliar.html.j2", id_filme=id_filme)
        else:
            return redirect(url_for('filme.editar_avaliacao', id_filme=id_filme))
    if request.method == "POST":
        if (len(Avaliacao.query.filter_by(id_usuario = id_usuario, id_filme=id_filme).all()) > 0):
            flash("Você já tem uma avaliação para esse filme")
            return redirect(url_for('filme.lista'))
        titulo = request.form.get('titulo')
        corpo = request.form.get('corpo')
        estrelas = request.form.get('estrelas')
        avaliacao = Avaliacao(titulo, corpo, estrelas, id_filme, id_usuario)
        db.session.add(avaliacao)
        db.session.commit()
        flash("Avaliação adicionada com sucesso")
        return redirect(url_for('filme.lista'))


@filme.route("<id_filme>/avaliacao/editar", methods=["GET", "POST"])
@login_required()
def editar_avaliacao(id_filme):
    id_usuario = current_user.id
    avaliacao = Avaliacao.query.filter_by(id_usuario=id_usuario, id_filme=id_filme).all()[0]
    if request.method == "GET":
        return render_template("editar_avaliacao.html.j2", avaliacao=avaliacao)
    if request.method == "POST":
        avaliacao.titulo = request.form.get('titulo')
        avaliacao.corpo = request.form.get('corpo')
        avaliacao.estrelas = request.form.get('estrelas')
        db.session.commit()
        flash("Avaliação editada com sucesso")
        return redirect(url_for('filme.lista'))


@filme.route("<id_filme>/avaliacao")
@login_required()
def visualizar_avaliacao(id_filme):
    id_usuario = current_user.id
    avaliacao = Avaliacao.query.filter_by(id_usuario=id_usuario, id_filme=id_filme).all()[0]
    return redirect(url_for('filme.editar_avaliacao'))


@filme.route("<id_filme>/avaliacao/deletar")
@login_required()
def deletar_avaliacao(id_filme):
    id_usuario = current_user.id
    avaliacao = Avaliacao.query.filter_by(id_usuario=id_usuario, id_filme=id_filme).all()[0]
    db.session.delete(avaliacao)
    db.session.commit()
    flash('Avaliação deletada com sucesso')
    return redirect(url_for('principal.index'))
