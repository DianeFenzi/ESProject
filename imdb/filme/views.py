from flask import Blueprint, request, url_for, redirect, render_template
from imdb import db
from imdb.filme.models import Filme

filme = Blueprint('filme', __name__, template_folder='templates')

################################################
#####              BLUEPRINT               #####
################################################

def list_movies():
    Filme
