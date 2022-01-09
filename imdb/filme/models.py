from imdb import db



class Filme(db.Model):

   __tablename__ = 'filme'
   id = db.Column(db.Integer, primary_key=True)

   titulo = db.Column(db.String(160), unique=True, nullable=False)
   id_imdb = db.Column(db.String(7), unique=True, nullable=False)
   atores = db.Column(db.String(1000), nullable=False)
   diretor = db.Column(db.String(160), nullable=False)


   def __init__(self, titulo, id_imdb, diretor, atores):
      if type(atores) == list:
          atores = ",".join(atores)
      self.titulo = titulo
      self.id_imdb = id_imdb
      self.diretor = diretor
      self.atores = atores

   def __repr__(self):
      return f"titulo:{self.titulo}"

# class Avaliacao(db.Model):
#
#     __tablename__ = 'avaliacao'
