from imdb import db
#from imdb.avaliacao.models import Avaliacao


class Filme(db.Model):

   __tablename__ = 'filme'
   id = db.Column(db.Integer, primary_key=True)

   titulo = db.Column(db.String(160), unique=True, nullable=False)
   id_imdb = db.Column(db.String(7), unique=True, nullable=False)
   atores = db.Column(db.String(1000), nullable=False)
   diretor = db.Column(db.String(160), nullable=False)
   avaliacoes = db.relationship('Avaliacao', cascade="all,delete", backref='filme', lazy= True)

   def __init__(self, titulo, id_imdb, diretor, atores):
      if type(atores) == list:
          atores = ",".join(atores)
      self.titulo = titulo
      self.id_imdb = id_imdb
      self.diretor = diretor
      self.atores = atores

   def media_avaliacao(self):
       media = 0
       avaliacoes = self.avaliacoes
       total = sum([avaliacao.estrelas for avaliacao in avaliacoes])
       if len(avaliacoes) > 0:
           media = total /len(avaliacoes)
       return media


   def __repr__(self):
      return f"titulo:{self.titulo}"






class Avaliacao(db.Model):
    __tablename__ = 'avaliacao'
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(200), nullable=False)
    corpo = db.Column(db.String(500))
    estrelas = db.Column(db.Integer, nullable=False)

    id_filme = db.Column(db.Integer, db.ForeignKey('filme.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __init__(self, titulo, corpo, estrelas, id_filme, id_usuario):
        self.titulo = titulo
        self.corpo = corpo
        self.estrelas = estrelas
        self.id_filme = id_filme
        self.id_usuario = id_usuario

    def __repr__(self):
       return f"titulo:{self.titulo}"
