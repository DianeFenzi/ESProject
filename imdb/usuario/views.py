from flask import Blueprint, request, url_for, redirect, render_template
from imdb import db
from imdb.usuario.models import Usuario

usuario = Blueprint('usuario', __name__, template_folder='templates')

@usuario.route("/cadastrar_usuario", methods=["GET","POST"])
def cadastrar_usuario():
   if request.method == "POST":
      usuario = Usuario(
         email=request.form["email"],
         senha=request.form["senha"],
         username=request.form["username"],
         funcao="usuario"
      )
      db.session.add(usuario)
      db.session.commit()
      return redirect(url_for('principal.index'))
   return render_template('cadastrar_usuario.html')


@usuario.route("/perfil", methods=["GET"])
def perfil():
    return render_template('perfil.html.j2')
