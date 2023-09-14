from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_openapi3 import OpenAPI, Info, Tag
import os

# Init app
# tags
home_tag = Tag(name="Documentation", description="Swagger, Redoc ou RapiDoc")
recipe_tag = Tag(
    name="Recipe", description="Add, view and delete recipes from the base")
info = Info(title="My Recipes API", version="1.0.0")
app = OpenAPI(__name__, info=info)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Recipe Class/Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    typ = db.Column(db.String(140))
    ingredients = db.Column(db.String(500))
    description = db.Column(db.String(500))
    
    def __init__(self, name, typ, ingredients, description):
        self.name = name
        self.typ = typ
        self.ingredients = ingredients
        self.description = description

# Recipe Schema

@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi.
    """
    return redirect('/openapi')


# Run Server

if __name__ == '__main__':
    app.run(debug=True)
