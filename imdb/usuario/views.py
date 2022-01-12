from flask import Blueprint, request, url_for, redirect, render_template, flash
from imdb import db, login_required
from imdb.usuario.models import Usuario

usuario = Blueprint('usuario', __name__, template_folder='templates')

@usuario.route("/cadastrar_usuario", methods=["GET","POST"])
def cadastrar_usuario():
   if request.method == "POST":
      usuario_existe = Usuario.query.filter(Usuario.email==request.form["email"]).first()
      if usuario_existe:
         flash("Email já cadastrado.")
         return redirect(url_for('usuario.cadastrar_usuario'))
      username_existe = Usuario.query.filter(Usuario.username==request.form["username"]).first()
      if username_existe:
         flash("Username já em uso.")
         return redirect(url_for('usuario.cadastrar_usuario'))
      usuario = Usuario(
         email=request.form["email"],
         senha=request.form["senha"],
         username=request.form["username"],
         funcao="usuario"
      )
      db.session.add(usuario)
      db.session.commit()
      return redirect(url_for('principal.index'))
   return render_template('cadastrar_usuario.html.j2')

@usuario.route("/perfil", methods=["GET"])
@login_required()
def perfil():
    return render_template('perfil.html.j2')
