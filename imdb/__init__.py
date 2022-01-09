# from functools import wraps
from flask import Flask, redirect, url_for, flash, current_app
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

login_manager = LoginManager()

app = Flask(__name__, static_url_path="/static")

app.config['SECRET_KEY'] = 'jaçgjfçsdajFAJSLÇJFOAofajsdfjpasfFAWIJeo40569masdmf'

##################################################################
######################### BANCO DE DADOS #########################
##################################################################

app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///storage.db"
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#                                              "pool_recycle": 10
#                                           }
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db, compare_type = True)


#################################################################
###################### CONFIGURA LOGIN ##########################
#################################################################

login_manager.init_app(app)
login_manager.login_view = "principal.login"
login_manager.login_message = "Não foi possível acessar esta página ou executar esta ação. Por favor confira se o login foi feito ou se você tem a devida permissão."

def login_required(role=["ANY"]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
               return current_app.login_manager.unauthorized()
            funcao = current_user.funcao
            if ((funcao not in role) and (role != ["ANY"])):
                flash("Você não tem permissão para acessar essa página.")
                return redirect(url_for('principal.index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def admin_required(role=["admin"]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return current_app.login_manager.unauthorized()
            funcao = current_user.funcao
            if ((funcao not in role) and (role != ["admin"])):
                flash("Você não tem permissão para acessar essa página.")
                return redirect(url_for('principal.index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

#################################################################
########################## MODELS ###############################
#################################################################

# from imdb.usuario.models.usuario import Usuario
# from imdb.aluno.models.aluno import Aluno
# from imdb.treinador.models.treinador import Treinador
# from imdb.treino.models.treino import Treino

#################################################################
########################## BLUEPRINTS ###########################
#################################################################

from imdb.principal.views import principal
from imdb.usuario.views import usuario
from imdb.filme.views import filme


app.register_blueprint(principal)
app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(filme, url_prefix='/filme')
