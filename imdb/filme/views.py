from flask import Blueprint, request, url_for, redirect, render_template, flash
from imdb import db, login_required, admin_required
from imdb.filme.models import Filme

filme = Blueprint('filme', __name__, template_folder='templates')

################################################
#####              BLUEPRINT               #####
################################################

@filme.route("/", methods=["GET", "POST"])
def lista():
    filmes = []
    if request.method == "POST":
        busca = request.form.get("busca")
        filmes += Filme.query.filter(Filme.titulo.like(f"%{busca}%"))
        filmes += Filme.query.filter(Filme.id_imdb.like(f"%{busca}%"))
        filmes += Filme.query.filter(Filme.diretor.like(f"%{busca}%"))
        filmes += Filme.query.filter(Filme.atores.like(f"%{busca}%"))
    else:
        filmes = Filme.query.all()
    return render_template("lista.html.j2", filmes=filmes)

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
        flash("Filme criado com sucesso")
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
