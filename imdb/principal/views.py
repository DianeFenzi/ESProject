from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from imdb.usuario.models import Usuario
from imdb.filme.models import Filme, Avaliacao
from imdb import login_required

################################################
#####              BLUEPRINT               #####
################################################

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route("/")
def index():
   usuario = current_user
   numero_de_filmes = Filme.query.count()
   numero_de_avaliacoes = Avaliacao.query.count()
   if usuario.is_authenticated:
       # for avaliacao in usuario.avaliacoes:
           # avaliacao.filme_titulo
       return render_template("principal.html.j2", usuario=usuario,
        avaliacoes=usuario.avaliacoes, 
        numero_de_filmes=numero_de_filmes,
        numero_de_avaliacoes=numero_de_avaliacoes)
   else:
       return render_template("principal.html.j2", avalicoes=[],
       numero_de_filmes=numero_de_filmes,
       numero_de_avaliacoes=numero_de_avaliacoes)

@principal.route("/login", methods=["GET","POST"])
def login():
   if current_user.is_authenticated:
      flash("Usuário já se encontra logado.")
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
               flash("Usuário foi logado com sucesso!")
               return redirect(url_for('principal.index'))
         else:
               flash("A senha é inválida")
      else:
         flash('O usuário é inválido')
         return redirect(url_for('principal.login'))

   return render_template('login.html.j2')

@principal.route('/logout')
@login_required()
def logout():
   if (current_user):
      logout_user()
      flash(" O logout foi feito com sucesso!")
   else:
      flash("Você deve estar logado para deslogar!")
   return redirect(url_for('principal.login'))
