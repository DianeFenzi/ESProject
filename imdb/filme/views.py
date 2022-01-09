from flask import Blueprint, request, url_for, redirect, render_template
from imdb import db
from imdb.filme.models import Filme

filme = Blueprint('filme', __name__, template_folder='templates')

################################################
#####              BLUEPRINT               #####
################################################

@filme.route("/filmes")
def lista():
    filmes = Filme.query.all()
    return render_template("lista.html.j2", filmes=filmes)
