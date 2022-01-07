from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from imdb.usuario.models import Usuario
from imdb import login_required

################################################
#####              BLUEPRINT               #####
################################################

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route("/")
def index():
   return "Hello World!"

@principal.route("/login", methods=["GET","POST"])
def login():
   if current_user.is_authenticated:
      flash("Usuário já logado.")
      return redirect(url_for('principal.index'))

   if request.method == 'POST':
      form = request.form

      email = form["email"]
      senha = form["senha"]

      usuario = Usuario.query.filter_by(email=email).first()
      
      if usuario:
         checaSenha = usuario.checa_senha(senha)
         
         if (checaSenha):
               login_user(usuario)
               print(current_user.funcao)
               flash("Usuário logado com sucesso!")
               return redirect(url_for('principal.index'))
         else:
               flash("Senha inválida")
      else:
         flash('Usuário inválido')
         return redirect(url_for('principal.login'))

   return render_template('login.html')

@principal.route('/logout')
@login_required()
def logout():
   if (current_user):
      logout_user()
      flash("Logout feito com sucesso!")
   else:
      flash("Você precisa estar logado para deslogar")
   return redirect(url_for('principal.login'))