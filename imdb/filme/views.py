from flask import Blueprint, request, url_for, redirect, render_template, flash
from imdb import db, login_required
from imdb.filme.models import Filme

filme = Blueprint('filme', __name__, template_folder='templates')

################################################
#####              BLUEPRINT               #####
################################################

@filme.route("/")
def lista():
    filmes = Filme.query.all()
    return render_template("lista.html.j2", filmes=filmes)

@filme.route("/adicionar/")
@login_required()
def adicionar():
    return render_template("adicionar.html.j2")

@filme.route("/editar/")
@login_required()
def editar(filme_id):
    return render_template("editar.html.j2")


@filme.route("/remover/<filme_id>")
@login_required()
def remover(filme_id):
    filme = Filme.query.get(filme_id)
    db.session.delete(filme)
    db.session.commit()
    flash("Filme removido com sucesso")
    return redirect(url_for('filme.lista'))
