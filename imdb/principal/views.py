from flask import Blueprint

################################################
#####              BLUEPRINT               #####
################################################

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route("/")
def index():
   return "Hello World!"