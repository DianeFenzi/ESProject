from imdb import db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from imdb.filme.models import Avaliacao


#################################################
#####             USER LOADER               #####
#################################################

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)


#################################################
#####            TABELA USUÁRIO             #####
#################################################

class Usuario(db.Model, UserMixin):

   bcrypt = Bcrypt()
#from imdb.avaliacao.models import Avaliacao

   __tablename__ = 'usuario'
   id = db.Column(db.Integer, primary_key=True)

   email = db.Column(db.String(80), unique=True, nullable=False)
   username = db.Column(db.String(80), unique=True, nullable=False)
   senha = db.Column(db.String(255),nullable = False)
   funcao = db.Column(db.String(50), server_default="user", nullable=False) #admin ou normal


   avaliacoes = db.relationship(Avaliacao, backref='usuario', lazy= True)


   def __init__(self, email, senha, username, funcao):
      self.username = username
      self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')
      self.email = email
      self.funcao = funcao

   def checa_senha(self, senha):
      return self.bcrypt.check_password_hash(self.senha,senha)

   def setSenha(self, senha):
      self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')

   def __repr__(self):
      return f"username:{self.username}"
